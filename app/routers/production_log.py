from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/production-logs", tags=["Production Logs"])

@router.get("/", response_model=list[schemas.ProductionLogResponse])
def get_logs(db: Session = Depends(get_db)):
    return db.query(models.ProductionLog).all()

@router.get("/{log_id}", response_model=schemas.ProductionLogResponse)
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.ProductionLog)\
        .filter(models.ProductionLog.id == log_id)\
        .first()
    if not log:
        raise HTTPException(status_code=404, detail="Production log tidak ditemukan")
    return log

@router.post("/", response_model=schemas.ProductionLogResponse)
def create_log(data: schemas.ProductionLogCreate, db: Session = Depends(get_db)):

    if not db.query(models.Worker).filter(models.Worker.id == data.worker_id).first():
        raise HTTPException(status_code=404, detail="Worker tidak ditemukan")

    if not db.query(models.Position).filter(models.Position.id == data.position_id).first():
        raise HTTPException(status_code=404, detail="Position tidak ditemukan")

    if data.sub_position_id is not None:
        if not db.query(models.SubPosition)\
            .filter(models.SubPosition.id == data.sub_position_id)\
            .first():
            raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")

    if not db.query(models.Shift).filter(models.Shift.id == data.shift_id).first():
        raise HTTPException(status_code=404, detail="Shift tidak ditemukan")

    if data.supplier_id is not None:
        if not db.query(models.Supplier).filter(models.Supplier.id == data.supplier_id).first():
            raise HTTPException(status_code=404, detail="Supplier tidak ditemukan")

    if not db.query(models.Item).filter(models.Item.id == data.item_id).first():
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    if data.problem_comment_id is not None:
        if not db.query(models.ProblemComment)\
            .filter(models.ProblemComment.id == data.problem_comment_id)\
            .first():
            raise HTTPException(status_code=404, detail="Problem comment tidak ditemukan")

    log = models.ProductionLog(**data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.put("/{log_id}", response_model=schemas.ProductionLogResponse)
def update_log(log_id: int, data: schemas.ProductionLogUpdate, db: Session = Depends(get_db)):
    log = db.query(models.ProductionLog)\
        .filter(models.ProductionLog.id == log_id)\
        .first()
    if not log:
        raise HTTPException(status_code=404, detail="Production log tidak ditemukan")
    
    # Verify foreign keys if they are being updated
    if data.worker_id:
        worker = db.query(models.Worker).filter(models.Worker.id == data.worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker tidak ditemukan")
    
    if data.position_id:
        position = db.query(models.Position).filter(models.Position.id == data.position_id).first()
        if not position:
            raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    if data.sub_position_id is not None:
        sub_position = db.query(models.SubPosition).filter(models.SubPosition.id == data.sub_position_id).first()
        if not sub_position:
            raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")
    
    if data.shift_id:
        shift = db.query(models.Shift).filter(models.Shift.id == data.shift_id).first()
        if not shift:
            raise HTTPException(status_code=404, detail="Shift tidak ditemukan")
    
    if data.supplier_id:
        supplier = db.query(models.Supplier).filter(models.Supplier.id == data.supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier tidak ditemukan")
    
    if data.item_id:
        item = db.query(models.Item).filter(models.Item.id == data.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    if data.problem_comment_id:
        problem_comment = db.query(models.ProblemComment).filter(models.ProblemComment.id == data.problem_comment_id).first()
        if not problem_comment:
            raise HTTPException(status_code=404, detail="Problem comment tidak ditemukan")
    
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(log, field, value)
    
    db.commit()
    db.refresh(log)
    return log

@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.ProductionLog)\
        .filter(models.ProductionLog.id == log_id)\
        .first()
    if not log:
        raise HTTPException(status_code=404, detail="Production log tidak ditemukan")
    
    db.delete(log)
    db.commit()
    return {"message": "Production log berhasil dihapus"}
