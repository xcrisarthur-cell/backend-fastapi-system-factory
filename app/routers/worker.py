from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.get("/", response_model=list[schemas.WorkerResponse])
def get_workers(db: Session = Depends(get_db)):
    return db.query(models.Worker).all()

@router.get("/{worker_id}", response_model=schemas.WorkerResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(models.Worker)\
        .filter(models.Worker.id == worker_id)\
        .first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker tidak ditemukan")
    return worker

@router.post("/", response_model=schemas.WorkerResponse)
def create_worker(data: schemas.WorkerCreate, db: Session = Depends(get_db)):
    # Validate position exists
    position = db.query(models.Position).filter(models.Position.id == data.position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    worker = models.Worker(**data.dict())
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker

@router.put("/{worker_id}", response_model=schemas.WorkerResponse)
def update_worker(worker_id: int, data: schemas.WorkerUpdate, db: Session = Depends(get_db)):
    worker = db.query(models.Worker)\
        .filter(models.Worker.id == worker_id)\
        .first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker tidak ditemukan")
    
    # Validate position exists if position_id is being updated
    if data.position_id is not None:
        position = db.query(models.Position).filter(models.Position.id == data.position_id).first()
        if not position:
            raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(worker, field, value)
    
    db.commit()
    db.refresh(worker)
    return worker

@router.delete("/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(models.Worker)\
        .filter(models.Worker.id == worker_id)\
        .first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker tidak ditemukan")
    
    db.delete(worker)
    db.commit()
    return {"message": "Worker berhasil dihapus"}
