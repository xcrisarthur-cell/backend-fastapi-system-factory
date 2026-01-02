import random
from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_data():
    db = SessionLocal()
    try:
        print("Starting seeding process...")

        # 1. Ensure Dependencies Exist
        
        # Division
        division = db.query(models.Division).first()
        if not division:
            print("Creating default Division...")
            division = models.Division(code="DIV-SEED", name="Seeder Division")
            db.add(division)
            db.commit()
            db.refresh(division)
        
        # Department
        department = db.query(models.Department).first()
        if not department:
            print("Creating default Department...")
            department = models.Department(division_id=division.id, code="DEPT-SEED", name="Seeder Department")
            db.add(department)
            db.commit()
            db.refresh(department)
            
        # Position
        position = db.query(models.Position).first()
        if not position:
            print("Creating default Position...")
            position = models.Position(code="POS-SEED", unit="pcs")
            db.add(position)
            db.commit()
            db.refresh(position)
            
        # SubPosition
        sub_position = db.query(models.SubPosition).first()
        if not sub_position:
            print("Creating default SubPosition...")
            sub_position = models.SubPosition(position_id=position.id, code="SUB-SEED")
            db.add(sub_position)
            db.commit()
            db.refresh(sub_position)
            
        # Worker
        worker = db.query(models.Worker).first()
        if not worker:
            print("Creating default Worker...")
            worker = models.Worker(name="Seeder Worker", position_id=position.id, department_id=department.id)
            db.add(worker)
            db.commit()
            db.refresh(worker)

        # Shift
        shift = db.query(models.Shift).first()
        if not shift:
            print("Creating default Shift...")
            shift = models.Shift(name="Shift 1")
            db.add(shift)
            db.commit()
            db.refresh(shift)
            
        # Supplier
        supplier = db.query(models.Supplier).first()
        if not supplier:
            print("Creating default Supplier...")
            supplier = models.Supplier(name="Seeder Supplier")
            db.add(supplier)
            db.commit()
            db.refresh(supplier)
            
        # Item
        item = db.query(models.Item).first()
        if not item:
            print("Creating default Item...")
            item = models.Item(item_number="ITEM-SEED", item_name="Seeder Item")
            db.add(item)
            db.commit()
            db.refresh(item)
            
        print("Dependencies check completed.")

        # Refresh lists for random selection
        positions = db.query(models.Position).all()
        sub_positions = db.query(models.SubPosition).all()
        workers = db.query(models.Worker).all()
        shifts = db.query(models.Shift).all()
        suppliers = db.query(models.Supplier).all()
        items = db.query(models.Item).all()
        
        # 2. Seed Problem Comments (10 data)
        print("Seeding Problem Comments...")
        problem_comments = []
        for i in range(10):
            description = f"Problem Comment Seeder {random.randint(1000, 9999)}"
            # Check uniqueness
            while db.query(models.ProblemComment).filter(models.ProblemComment.description == description).first():
                description = f"Problem Comment Seeder {random.randint(1000, 9999)}"
            
            pc = models.ProblemComment(description=description)
            db.add(pc)
            problem_comments.append(pc)
        db.commit()
        for pc in problem_comments:
            db.refresh(pc)
        print("Seeding Problem Comments completed.")

        # 3. Seed Production Targets (10 data)
        print("Seeding Production Targets...")
        for i in range(10):
            target_pos = random.choice(positions)
            # Find sub_positions belonging to this position, or None
            valid_subs = [sp for sp in sub_positions if sp.position_id == target_pos.id]
            target_sub = random.choice(valid_subs) if valid_subs else None
            
            pt = models.ProductionTarget(
                target=random.randint(100, 1000),
                position_id=target_pos.id,
                sub_position_id=target_sub.id if target_sub else None
            )
            db.add(pt)
        db.commit()
        print("Seeding Production Targets completed.")

        # 4. Seed Attendances (10 data)
        print("Seeding Attendances...")
        for i in range(10):
            attendance_worker = random.choice(workers)
            att_date = datetime.now().date() - timedelta(days=i)
            att_time = time(hour=random.randint(7, 9), minute=random.randint(0, 59))
            
            att = models.Attendance(
                worker_id=attendance_worker.id,
                status=random.choice(["HADIR", "IJIN", "CUTI", "ALPA"]),
                date=att_date,
                time=att_time,
                notes=f"Seeder Note {i}",
                approved_coordinator=random.choice([True, False]),
                approved_supervisor=random.choice([True, False])
            )
            db.add(att)
        db.commit()
        print("Seeding Attendances completed.")

        # 5. Seed Production Logs (10 data)
        print("Seeding Production Logs...")
        for i in range(10):
            log_worker = random.choice(workers)
            log_pos = random.choice(positions)
            # Try to match sub_position to position if possible, otherwise just pick one or None
            valid_subs = [sp for sp in sub_positions if sp.position_id == log_pos.id]
            log_sub = random.choice(valid_subs) if valid_subs else None
            
            # Determine approvals based on constraint: (approved_spv IS NULL) OR (approved_coordinator = true)
            approved_coordinator = random.choice([True, False, None])
            
            approved_spv = None
            if approved_coordinator is True:
                approved_spv = random.choice([True, False, None])
            
            log = models.ProductionLog(
                worker_id=log_worker.id,
                position_id=log_pos.id,
                sub_position_id=log_sub.id if log_sub else None,
                shift_id=random.choice(shifts).id,
                supplier_id=random.choice(suppliers).id if suppliers else None,
                item_id=random.choice(items).id,
                qty_output=random.randint(50, 200),
                qty_reject=random.randint(0, 10),
                problem_duration_minutes=random.randint(0, 60),
                created_at=datetime.now() - timedelta(hours=i),
                approved_coordinator=approved_coordinator,
                approved_spv=approved_spv
            )
            db.add(log)
            db.flush() # to get log.id
            
            # Add random problem comments
            if problem_comments:
                num_comments = random.randint(0, 3)
                selected_comments = random.sample(problem_comments, num_comments)
                for pc in selected_comments:
                    plpc = models.ProductionLogProblemComment(
                        production_log_id=log.id,
                        problem_comment_id=pc.id
                    )
                    db.add(plpc)
                    
        db.commit()
        print("Seeding Production Logs completed.")
        
        print("All seeding tasks completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
