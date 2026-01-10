from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=list[schemas.ItemResponse])
@router.get("/", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    """Get all items"""
    return db.query(models.Item).all()


@router.get("/{item_identifier}", response_model=schemas.ItemResponse)
@router.get("/{item_identifier}/", response_model=schemas.ItemResponse)
def get_item_by_id_or_number(item_identifier: str, db: Session = Depends(get_db)):
    """Get an item by ID (integer) or item_number (string)"""
    # Try to parse as integer first (for backward compatibility with ID lookup)
    try:
        item_id = int(item_identifier)
        item = db.query(models.Item)\
            .filter(models.Item.id == item_id)\
            .first()
        if item:
            return item
    except ValueError:
        pass  # Not an integer, will try as item_number
    
    # Try as item_number
    item = db.query(models.Item)\
        .filter(models.Item.item_number == item_identifier)\
        .first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    return item


@router.get("/number/{item_number}", response_model=schemas.ItemResponse)
@router.get("/number/{item_number}/", response_model=schemas.ItemResponse)
def get_item(item_number: str, db: Session = Depends(get_db)):
    """Get an item by item number"""
    item = db.query(models.Item)\
        .filter(models.Item.item_number == item_number)\
        .first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    return item


@router.post("", response_model=schemas.ItemResponse, status_code=201)
@router.post("/", response_model=schemas.ItemResponse, status_code=201)
def create_item(data: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Create a new item"""
    # Check if item_number already exists
    exists = db.query(models.Item)\
        .filter(models.Item.item_number == data.item_number)\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Item number sudah ada")
    
    item = models.Item(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=schemas.ItemResponse)
@router.put("/{item_id}/", response_model=schemas.ItemResponse)
def update_item(item_id: int, data: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """Update an item by ID"""
    item = db.query(models.Item)\
        .filter(models.Item.id == item_id)\
        .first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    # Check if new item_number conflicts with existing
    if data.item_number and data.item_number != item.item_number:
        exists = db.query(models.Item)\
            .filter(models.Item.item_number == data.item_number)\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Item number sudah ada")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
@router.delete("/{item_id}/")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item by ID"""
    item = db.query(models.Item)\
        .filter(models.Item.id == item_id)\
        .first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    db.delete(item)
    db.commit()
    return {"message": "Item berhasil dihapus"}
