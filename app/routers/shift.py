from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/shifts", tags=["Shifts"])


@router.get("/", response_model=list[schemas.ShiftResponse])
def get_shifts(db: Session = Depends(get_db)):
    """Get all shifts"""
    return db.query(models.Shift).all()


@router.get("/{shift_id}", response_model=schemas.ShiftResponse)
def get_shift(shift_id: int, db: Session = Depends(get_db)):
    """Get a shift by ID"""
    shift = db.query(models.Shift)\
        .filter(models.Shift.id == shift_id)\
        .first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift tidak ditemukan")
    return shift


@router.post("/", response_model=schemas.ShiftResponse, status_code=201)
def create_shift(data: schemas.ShiftCreate, db: Session = Depends(get_db)):
    """Create a new shift"""
    # Check if name already exists
    exists = db.query(models.Shift)\
        .filter(models.Shift.name == data.name)\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Shift name sudah ada")
    
    shift = models.Shift(**data.model_dump())
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift


@router.put("/{shift_id}", response_model=schemas.ShiftResponse)
def update_shift(shift_id: int, data: schemas.ShiftUpdate, db: Session = Depends(get_db)):
    """Update a shift"""
    shift = db.query(models.Shift)\
        .filter(models.Shift.id == shift_id)\
        .first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift tidak ditemukan")
    
    # Check if new name conflicts with existing
    if data.name and data.name != shift.name:
        exists = db.query(models.Shift)\
            .filter(models.Shift.name == data.name)\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Shift name sudah ada")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shift, field, value)
    
    db.commit()
    db.refresh(shift)
    return shift


@router.delete("/{shift_id}")
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    """Delete a shift"""
    shift = db.query(models.Shift)\
        .filter(models.Shift.id == shift_id)\
        .first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift tidak ditemukan")
    
    db.delete(shift)
    db.commit()
    return {"message": "Shift berhasil dihapus"}
