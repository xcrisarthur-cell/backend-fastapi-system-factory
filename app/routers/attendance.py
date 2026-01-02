from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/attendances", tags=["Attendances"])


@router.get("", response_model=list[schemas.AttendanceResponse])
@router.get("/", response_model=list[schemas.AttendanceResponse])
def get_attendances(db: Session = Depends(get_db)):
    """Get all attendances"""
    return db.query(models.Attendance)\
        .options(joinedload(models.Attendance.worker))\
        .all()


@router.get("/{attendance_id}", response_model=schemas.AttendanceResponse)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    """Get an attendance by ID"""
    attendance = db.query(models.Attendance)\
        .options(joinedload(models.Attendance.worker))\
        .filter(models.Attendance.id == attendance_id)\
        .first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance tidak ditemukan")
    return attendance


@router.post("/", response_model=schemas.AttendanceResponse, status_code=201)
def create_attendance(data: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    """Create a new attendance record"""
    try:
        # Validate worker exists
        worker = db.query(models.Worker).filter(models.Worker.id == data.worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker tidak ditemukan")

        new_attendance = models.Attendance(**data.model_dump())
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        
        return db.query(models.Attendance)\
            .options(joinedload(models.Attendance.worker))\
            .filter(models.Attendance.id == new_attendance.id)\
            .first()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating attendance: {str(e)}")


@router.put("/{attendance_id}", response_model=schemas.AttendanceResponse)
def update_attendance(attendance_id: int, data: schemas.AttendanceUpdate, db: Session = Depends(get_db)):
    """Update an attendance record"""
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance tidak ditemukan")
    
    # Validate worker if changed
    if data.worker_id is not None:
        worker = db.query(models.Worker).filter(models.Worker.id == data.worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker tidak ditemukan")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(attendance, field, value)
    
    try:
        db.commit()
        db.refresh(attendance)
        return db.query(models.Attendance)\
            .options(joinedload(models.Attendance.worker))\
            .filter(models.Attendance.id == attendance.id)\
            .first()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating attendance: {str(e)}")


@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    """Delete an attendance record"""
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance tidak ditemukan")
    
    try:
        db.delete(attendance)
        db.commit()
        return {"message": "Attendance berhasil dihapus"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting attendance: {str(e)}")
