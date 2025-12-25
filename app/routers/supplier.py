from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.get("/", response_model=list[schemas.SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(models.Supplier).all()

@router.get("/{supplier_id}", response_model=schemas.SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(models.Supplier)\
        .filter(models.Supplier.id == supplier_id)\
        .first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier tidak ditemukan")
    return supplier

@router.post("/", response_model=schemas.SupplierResponse)
def create_supplier(data: schemas.SupplierCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Supplier)\
        .filter(models.Supplier.name == data.name)\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Supplier sudah ada")

    supplier = models.Supplier(**data.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.put("/{supplier_id}", response_model=schemas.SupplierResponse)
def update_supplier(supplier_id: int, data: schemas.SupplierUpdate, db: Session = Depends(get_db)):
    supplier = db.query(models.Supplier)\
        .filter(models.Supplier.id == supplier_id)\
        .first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier tidak ditemukan")
    
    # Check if new name conflicts with existing
    if data.name and data.name != supplier.name:
        exists = db.query(models.Supplier)\
            .filter(models.Supplier.name == data.name)\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Supplier name sudah ada")
    
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.commit()
    db.refresh(supplier)
    return supplier

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(models.Supplier)\
        .filter(models.Supplier.id == supplier_id)\
        .first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier tidak ditemukan")
    
    db.delete(supplier)
    db.commit()
    return {"message": "Supplier berhasil dihapus"}
