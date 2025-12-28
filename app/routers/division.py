from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/divisions", tags=["Divisions"])


@router.get("/", response_model=list[schemas.DivisionResponse])
def get_divisions(db: Session = Depends(get_db)):
    """Get all divisions"""
    return db.query(models.Division).all()


@router.get("/{division_id}", response_model=schemas.DivisionResponse)
def get_division(division_id: int, db: Session = Depends(get_db)):
    """Get a division by ID"""
    division = db.query(models.Division)\
        .filter(models.Division.id == division_id)\
        .first()
    if not division:
        raise HTTPException(status_code=404, detail="Division tidak ditemukan")
    return division


@router.post("/", response_model=schemas.DivisionResponse, status_code=201)
def create_division(data: schemas.DivisionCreate, db: Session = Depends(get_db)):
    """Create a new division"""
    # Check if code already exists
    exists = db.query(models.Division)\
        .filter(models.Division.code == data.code)\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Division code sudah ada")
    
    # Check if name already exists
    exists = db.query(models.Division)\
        .filter(models.Division.name == data.name)\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Division name sudah ada")

    division = models.Division(**data.model_dump())
    db.add(division)
    db.commit()
    db.refresh(division)
    return division


@router.put("/{division_id}", response_model=schemas.DivisionResponse)
def update_division(division_id: int, data: schemas.DivisionUpdate, db: Session = Depends(get_db)):
    """Update a division"""
    division = db.query(models.Division)\
        .filter(models.Division.id == division_id)\
        .first()
    if not division:
        raise HTTPException(status_code=404, detail="Division tidak ditemukan")
    
    # Check if new code conflicts with existing
    if data.code and data.code != division.code:
        exists = db.query(models.Division)\
            .filter(models.Division.code == data.code)\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Division code sudah ada")
    
    # Check if new name conflicts with existing
    if data.name and data.name != division.name:
        exists = db.query(models.Division)\
            .filter(models.Division.name == data.name)\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Division name sudah ada")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(division, field, value)
    
    db.commit()
    db.refresh(division)
    return division


@router.delete("/{division_id}")
def delete_division(division_id: int, db: Session = Depends(get_db)):
    """Delete a division"""
    division = db.query(models.Division)\
        .filter(models.Division.id == division_id)\
        .first()
    if not division:
        raise HTTPException(status_code=404, detail="Division tidak ditemukan")
    
    db.delete(division)
    db.commit()
    return {"message": "Division berhasil dihapus"}

