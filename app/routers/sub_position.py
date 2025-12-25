from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/sub-positions", tags=["Sub Positions"])

@router.get("/", response_model=list[schemas.SubPositionResponse])
def get_sub_positions(db: Session = Depends(get_db)):
    return db.query(models.SubPosition).all()

@router.get("/{sub_position_id}", response_model=schemas.SubPositionResponse)
def get_sub_position(sub_position_id: int, db: Session = Depends(get_db)):
    sub_position = db.query(models.SubPosition)\
        .filter(models.SubPosition.id == sub_position_id)\
        .first()
    if not sub_position:
        raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")
    return sub_position

@router.get("/by-position/{position_id}", response_model=list[schemas.SubPositionResponse])
def get_by_position(position_id: int, db: Session = Depends(get_db)):
    return db.query(models.SubPosition)\
        .filter(models.SubPosition.position_id == position_id)\
        .all()

@router.post("/", response_model=schemas.SubPositionResponse)
def create_sub_position(data: schemas.SubPositionCreate, db: Session = Depends(get_db)):
    # Verify position exists
    position = db.query(models.Position)\
        .filter(models.Position.id == data.position_id)\
        .first()
    if not position:
        raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    sub = models.SubPosition(**data.dict())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

@router.put("/{sub_position_id}", response_model=schemas.SubPositionResponse)
def update_sub_position(sub_position_id: int, data: schemas.SubPositionUpdate, db: Session = Depends(get_db)):
    sub_position = db.query(models.SubPosition)\
        .filter(models.SubPosition.id == sub_position_id)\
        .first()
    if not sub_position:
        raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")
    
    # Verify position exists if updating position_id
    if data.position_id:
        position = db.query(models.Position)\
            .filter(models.Position.id == data.position_id)\
            .first()
        if not position:
            raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sub_position, field, value)
    
    db.commit()
    db.refresh(sub_position)
    return sub_position

@router.delete("/{sub_position_id}")
def delete_sub_position(sub_position_id: int, db: Session = Depends(get_db)):
    sub_position = db.query(models.SubPosition)\
        .filter(models.SubPosition.id == sub_position_id)\
        .first()
    if not sub_position:
        raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")
    
    db.delete(sub_position)
    db.commit()
    return {"message": "Sub position berhasil dihapus"}
