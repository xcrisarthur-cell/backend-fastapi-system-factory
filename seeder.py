import re
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.security import hash_password

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_key_value(text):
    """
    Parses string like "(key1=value1, key2=value2)" into a dictionary.
    Handles values that might contain spaces.
    """
    if not text:
        return {}
    
    # Remove surrounding parentheses
    text = text.strip()
    if text.startswith('(') and text.endswith(')'):
        text = text[1:-1]
    
    # Split by comma, but be careful about commas in values? 
    # The format seems to be key=value spec=value (space separated if not comma)
    # Let's look at the file content again.
    # - W8320015073176 (item_name=SPRING POCKET 15X073X176 spec=KAWAT 2.00 MM)
    # Here there is no comma between item_name value and spec key.
    # - SLAMET PURNOMO (position=PER, departments=operator)
    # Here there is a comma.
    
    # Strategy: split by known keys.
    known_keys = ['position', 'departments', 'sub_position', 'item_name', 'spec']
    
    # We can use regex to find " key=" patterns
    # But first, let's try to identify if comma is used as separator.
    
    data = {}
    
    # Special handling for Item lines which might mix comma and space
    # For workers: position=PER, departments=operator (comma separated)
    # For items: item_name=... spec=... (space separated, no comma before spec)
    
    # Let's try a regex that looks for key=value pairs
    # pattern: (key)=(.+?)(?=\s+\w+=|$) -> look ahead for next key or end of string
    # But for comma separated: (key)=(.+?)(?:,\s*|$)
    
    # Let's clean the text first
    text = text.strip()
    
    # Check if we have "spec="
    spec_match = re.search(r'spec=(.*)', text)
    if spec_match:
        data['spec'] = spec_match.group(1).strip()
        text = text[:spec_match.start()].strip() # Remove spec part
    
    # Check if we have "item_name="
    item_name_match = re.search(r'item_name=(.*)', text)
    if item_name_match:
        # If spec was present, we removed it. If not, it takes till end.
        # But wait, if there are other keys?
        # Items only have item_name and spec.
        val = item_name_match.group(1).strip()
        # Remove trailing comma if any (from previous logic if mixed)
        if val.endswith(','): val = val[:-1]
        data['item_name'] = val
        return data

    # For others (comma separated)
    parts = [p.strip() for p in text.split(',')]
    for part in parts:
        if '=' in part:
            k, v = part.split('=', 1)
            data[k.strip()] = v.strip()
            
    return data

def seed_data():
    db = SessionLocal()
    try:
        print("Starting seeding process...")
        
        with open("seeder_ref.txt", "r") as f:
            lines = f.readlines()
            
        current_section = None
        
        # Caches to avoid DB lookups
        divisions_map = {} # name -> id
        departments_map = {} # name -> id
        positions_map = {} # name -> id (using UPPER name as key for lookup from other tables)
        sub_positions_map = {} # code -> id
        shifts_map = {} # name -> id
        suppliers_map = {} # name -> id
        
        # Pre-load existing data if any (optional, but good for idempotency)
        # For now, we'll just query as we go or rely on unique constraints?
        # Better to query as we go.
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("Tabel "):
                current_section = line
                print(f"Processing {current_section}...")
                continue
            
            if not line.startswith("-"):
                continue
                
            # Remove "- "
            content = line[2:].strip()
            
            if current_section == "Tabel Divisions":
                name = content
                code = name.upper()
                # Check if exists
                obj = db.query(models.Division).filter(models.Division.name == name).first()
                if not obj:
                    obj = models.Division(name=name, code=code)
                    db.add(obj)
                    db.commit()
                    db.refresh(obj)
                divisions_map[name] = obj.id
                
            elif current_section == "Tabel Departments":
                name = content
                code = name.upper().replace(" ", "_")
                # Assign to a default division (e.g. Kawat) unless it's specific
                # For simplicity, assign Superadmin to IT (if exists), others to Kawat
                div_id = None
                if name.upper() == "SUPERADMIN" and "IT" in divisions_map:
                    div_id = divisions_map["IT"]
                elif "Kawat" in divisions_map:
                    div_id = divisions_map["Kawat"]
                else:
                    # Fallback to first available division
                    div_id = list(divisions_map.values())[0] if divisions_map else None
                
                if div_id:
                    obj = db.query(models.Department).filter(models.Department.name == name).first()
                    if not obj:
                        obj = models.Department(name=name, code=code, division_id=div_id)
                        db.add(obj)
                        db.commit()
                        db.refresh(obj)
                    departments_map[name.lower()] = obj.id # Store as lower for case-insensitive lookup
            
            elif current_section == "Tabel Positions":
                # Format: Name (unit)
                # Example: Per (pcs)
                match = re.match(r'^(.*)\s+\((.*)\)$', content)
                if match:
                    name = match.group(1).strip()
                    unit = match.group(2).strip()
                    code = name.upper().replace(" ", "_")
                    
                    obj = db.query(models.Position).filter(models.Position.code == code).first()
                    if not obj:
                        obj = models.Position(name=name, code=code, unit=unit)
                        db.add(obj)
                        db.commit()
                        db.refresh(obj)
                    positions_map[code] = obj.id # Store by code (UPPER)
            
            elif current_section == "Tabel Sub Positions":
                # Format: Code (position=POSITION_NAME)
                # Example: FC60 (position=PER)
                match = re.match(r'^(.*)\s+\((.*)\)$', content)
                if match:
                    code = match.group(1).strip()
                    params = parse_key_value(f"({match.group(2)})")
                    pos_name = params.get('position')
                    
                    if pos_name and pos_name in positions_map:
                        pos_id = positions_map[pos_name]
                        obj = db.query(models.SubPosition).filter(models.SubPosition.code == code).first()
                        if not obj:
                            obj = models.SubPosition(code=code, position_id=pos_id)
                            db.add(obj)
                            db.commit()
                            db.refresh(obj)
                        sub_positions_map[code] = obj.id
            
            elif current_section == "Tabel Workers":
                # Format: Name (position=POS, departments=DEPT)
                # Example: SLAMET PURNOMO (position=PER, departments=operator)
                match = re.match(r'^(.*?)\s+\((.*)\)$', content)
                if match:
                    name = match.group(1).strip()
                    params = parse_key_value(f"({match.group(2)})")
                    pos_name = params.get('position')
                    dept_name = params.get('departments')
                    password_raw = params.get('password')
                    
                    pos_id = positions_map.get(pos_name) if pos_name else None
                    dept_id = departments_map.get(dept_name.lower()) if dept_name else None
                    
                    password_hash = None
                    if password_raw:
                        password_hash = hash_password(password_raw)
                    
                    obj = db.query(models.Worker).filter(models.Worker.name == name).first()
                    if not obj:
                        obj = models.Worker(
                            name=name, 
                            position_id=pos_id, 
                            department_id=dept_id,
                            password=password_hash
                        )
                        db.add(obj)
                        db.commit()
            
            elif current_section == "Tabel Shifts":
                name = content
                obj = db.query(models.Shift).filter(models.Shift.name == name).first()
                if not obj:
                    obj = models.Shift(name=name)
                    db.add(obj)
                    db.commit()
                    db.refresh(obj)
                shifts_map[name] = obj.id
            
            elif current_section == "Tabel Suppliers":
                name = content
                obj = db.query(models.Supplier).filter(models.Supplier.name == name).first()
                if not obj:
                    obj = models.Supplier(name=name)
                    db.add(obj)
                    db.commit()
            
            elif current_section == "Tabel Items":
                # Format: ItemNumber (item_name=NAME spec=SPEC)
                # Tab might be used
                # Example: W1090001581224 (item_name=PER T15 D8,1 K2,24)
                
                # Split by first opening parenthesis
                parts = content.split('(', 1)
                item_number = parts[0].strip()
                rest = parts[1] if len(parts) > 1 else ""
                if rest.endswith(')'): rest = rest[:-1]
                
                params = parse_key_value(f"({rest})")
                item_name = params.get('item_name')
                spec = params.get('spec')
                
                obj = db.query(models.Item).filter(models.Item.item_number == item_number).first()
                if not obj:
                    obj = models.Item(item_number=item_number, item_name=item_name, spec=spec)
                    db.add(obj)
                    db.commit()
            
            elif current_section == "Tabel Production Target":
                # Format: Target (position=POS, sub_position=SUB)
                # Example: 13000 (position=PER, sub_position=FC60)
                match = re.match(r'^(.*?)\s+\((.*)\)$', content)
                if match:
                    target_val = match.group(1).strip()
                    params = parse_key_value(f"({match.group(2)})")
                    pos_name = params.get('position')
                    sub_pos_code = params.get('sub_position')
                    
                    pos_id = positions_map.get(pos_name) if pos_name else None
                    sub_pos_id = sub_positions_map.get(sub_pos_code) if sub_pos_code else None
                    
                    # Check if exists (might be multiple targets, but assuming unique combination for now or just append)
                    # Actually ProductionTarget doesn't have unique constraint on pos/subpos.
                    # We'll just add it.
                    obj = models.ProductionTarget(
                        target=float(target_val),
                        position_id=pos_id,
                        sub_position_id=sub_pos_id
                    )
                    db.add(obj)
                    db.commit()

            elif current_section == "Tabel Problem Comments":
                desc = content
                obj = db.query(models.ProblemComment).filter(models.ProblemComment.description == desc).first()
                if not obj:
                    obj = models.ProblemComment(description=desc)
                    db.add(obj)
                    db.commit()

        print("Seeding completed successfully.")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
