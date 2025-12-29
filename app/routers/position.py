from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.get("", response_model=list[schemas.PositionResponse])
@router.get("/", response_model=list[schemas.PositionResponse])
def get_positions(db: Session = Depends(get_db)):
    """Get all positions"""
    return db.query(models.Position).all()


@router.get("/{position_id}", response_model=schemas.PositionResponse)
def get_position(position_id: int, db: Session = Depends(get_db)):
    """Get a position by ID"""
    position = db.query(models.Position)\
        .filter(models.Position.id == position_id)\
        .first()
    if not position:
        raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    return position


@router.post("/", response_model=schemas.PositionResponse, status_code=201)
def create_position(data: schemas.PositionCreate, db: Session = Depends(get_db)):
    """Create a new position"""
    if data.unit not in ["pcs", "lmbr"]:
        raise HTTPException(status_code=400, detail="Unit harus pcs atau lmbr")
    
    # Check if code already exists
    exists = db.query(models.Position)\
        .filter(models.Position.code == data.code)\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Position code sudah ada")

    position = models.Position(**data.model_dump())
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


@router.put("/{position_id}", response_model=schemas.PositionResponse)
def update_position(position_id: int, data: schemas.PositionUpdate, db: Session = Depends(get_db)):
    """Update a position"""
    position = db.query(models.Position)\
        .filter(models.Position.id == position_id)\
        .first()
    if not position:
        raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    if data.unit and data.unit not in ["pcs", "lmbr"]:
        raise HTTPException(status_code=400, detail="Unit harus pcs atau lmbr")
    
    # Check if new code conflicts with existing
    if data.code and data.code != position.code:
        exists = db.query(models.Position)\
            .filter(models.Position.code == data.code)\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Position code sudah ada")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(position, field, value)
    
    db.commit()
    db.refresh(position)
    return position


@router.delete("/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db)):
    """Delete a position"""
    position = db.query(models.Position)\
        .filter(models.Position.id == position_id)\
        .first()
    if not position:
        raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    db.delete(position)
    db.commit()
    return {"message": "Position berhasil dihapus"}
