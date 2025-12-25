from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@router.get("/{item_number}", response_model=schemas.ItemResponse)
def get_item(item_number: str, db: Session = Depends(get_db)):
    item = db.query(models.Item)\
        .filter(models.Item.item_number == item_number)\
        .first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    return item

@router.post("/", response_model=schemas.ItemResponse)
def create_item(data: schemas.ItemCreate, db: Session = Depends(get_db)):
    # Check if item_number already exists
    exists = db.query(models.Item)\
        .filter(models.Item.item_number == data.item_number)\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Item number sudah ada")
    
    item = models.Item(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/{item_number}", response_model=schemas.ItemResponse)
def update_item(item_number: str, data: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(models.Item)\
        .filter(models.Item.item_number == item_number)\
        .first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    # Check if new item_number conflicts with existing
    if data.item_number and data.item_number != item_number:
        exists = db.query(models.Item)\
            .filter(models.Item.item_number == data.item_number)\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Item number sudah ada")
    
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_number}")
def delete_item(item_number: str, db: Session = Depends(get_db)):
    item = db.query(models.Item)\
        .filter(models.Item.item_number == item_number)\
        .first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    db.delete(item)
    db.commit()
    return {"message": "Item berhasil dihapus"}
