from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/sub-positions", tags=["Sub Positions"])


@router.get("", response_model=list[schemas.SubPositionResponse])
@router.get("/", response_model=list[schemas.SubPositionResponse])
def get_sub_positions(db: Session = Depends(get_db)):
    """Get all sub positions with their position information"""
    return db.query(models.SubPosition)\
        .options(joinedload(models.SubPosition.position))\
        .all()


@router.get("/{sub_position_id}", response_model=schemas.SubPositionResponse)
@router.get("/{sub_position_id}/", response_model=schemas.SubPositionResponse)
def get_sub_position(sub_position_id: int, db: Session = Depends(get_db)):
    """Get a sub position by ID with position information"""
    sub_position = db.query(models.SubPosition)\
        .options(joinedload(models.SubPosition.position))\
        .filter(models.SubPosition.id == sub_position_id)\
        .first()
    if not sub_position:
        raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")
    return sub_position


@router.get("/by-position/{position_id}", response_model=list[schemas.SubPositionResponse])
@router.get("/by-position/{position_id}/", response_model=list[schemas.SubPositionResponse])
def get_by_position(position_id: int, db: Session = Depends(get_db)):
    """Get all sub positions by position ID"""
    return db.query(models.SubPosition)\
        .options(joinedload(models.SubPosition.position))\
        .filter(models.SubPosition.position_id == position_id)\
        .all()


@router.post("", response_model=schemas.SubPositionResponse, status_code=201)
@router.post("/", response_model=schemas.SubPositionResponse, status_code=201)
def create_sub_position(data: schemas.SubPositionCreate, db: Session = Depends(get_db)):
    """Create a new sub position"""
    # Verify position exists
    position = db.query(models.Position)\
        .filter(models.Position.id == data.position_id)\
        .first()
    if not position:
        raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    # Check if code already exists for this position
    exists = db.query(models.SubPosition)\
        .filter(
            models.SubPosition.position_id == data.position_id,
            models.SubPosition.code == data.code
        )\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Sub position code sudah ada untuk position ini")
    
    sub = models.SubPosition(**data.model_dump())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    
    # Reload with relationships
    return db.query(models.SubPosition)\
        .options(joinedload(models.SubPosition.position))\
        .filter(models.SubPosition.id == sub.id)\
        .first()


@router.put("/{sub_position_id}", response_model=schemas.SubPositionResponse)
@router.put("/{sub_position_id}/", response_model=schemas.SubPositionResponse)
def update_sub_position(sub_position_id: int, data: schemas.SubPositionUpdate, db: Session = Depends(get_db)):
    """Update a sub position"""
    sub_position = db.query(models.SubPosition)\
        .filter(models.SubPosition.id == sub_position_id)\
        .first()
    if not sub_position:
        raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")
    
    # Verify position exists if updating position_id
    if data.position_id is not None:
        position = db.query(models.Position)\
            .filter(models.Position.id == data.position_id)\
            .first()
        if not position:
            raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    # Check if new code conflicts with existing
    if data.code and data.code != sub_position.code:
        new_position_id = data.position_id if data.position_id is not None else sub_position.position_id
        exists = db.query(models.SubPosition)\
            .filter(
                models.SubPosition.position_id == new_position_id,
                models.SubPosition.code == data.code,
                models.SubPosition.id != sub_position_id
            )\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Sub position code sudah ada untuk position ini")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sub_position, field, value)
    
    db.commit()
    db.refresh(sub_position)
    
    # Reload with relationships
    return db.query(models.SubPosition)\
        .options(joinedload(models.SubPosition.position))\
        .filter(models.SubPosition.id == sub_position.id)\
        .first()


@router.delete("/{sub_position_id}")
@router.delete("/{sub_position_id}/")
def delete_sub_position(sub_position_id: int, db: Session = Depends(get_db)):
    """Delete a sub position"""
    sub_position = db.query(models.SubPosition)\
        .filter(models.SubPosition.id == sub_position_id)\
        .first()
    if not sub_position:
        raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")
    
    db.delete(sub_position)
    db.commit()
    return {"message": "Sub position berhasil dihapus"}
