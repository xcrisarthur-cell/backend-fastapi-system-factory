from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, selectinload
from datetime import datetime
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/production-logs", tags=["Production Logs"])


def _format_production_log_response(log: models.ProductionLog) -> schemas.ProductionLogResponse:
    """Helper function to format production log with problem_comments extracted"""
    # Extract problem_comments from the many-to-many relationship
    problem_comments = [
        pc.problem_comment for pc in log.production_log_problem_comments
        if pc.problem_comment
    ] if log.production_log_problem_comments else []
    
    # Create response dict
    log_dict = {
        "id": log.id,
        "worker_id": log.worker_id,
        "position_id": log.position_id,
        "sub_position_id": log.sub_position_id,
        "shift_id": log.shift_id,
        "supplier_id": log.supplier_id,
        "item_id": log.item_id,
        "qty_output": float(log.qty_output),
        "qty_reject": float(log.qty_reject),
        "problem_duration_minutes": log.problem_duration_minutes,
        "created_at": log.created_at,
        "approved_coordinator": log.approved_coordinator,
        "approved_spv": log.approved_spv,
        "approved_coordinator_at": log.approved_coordinator_at,
        "approved_spv_at": log.approved_spv_at,
        "approved_coordinator_by": log.approved_coordinator_by,
        "approved_spv_by": log.approved_spv_by,
        "worker": log.worker,
        "position": log.position,
        "sub_position": log.sub_position,
        "shift": log.shift,
        "supplier": log.supplier,
        "item": log.item,
        "approved_coordinator_by_worker": log.approved_coordinator_by_worker,
        "approved_spv_by_worker": log.approved_spv_by_worker,
        "problem_comments": problem_comments
    }
    return schemas.ProductionLogResponse.model_validate(log_dict)


@router.get("", response_model=list[schemas.ProductionLogResponse])
@router.get("/", response_model=list[schemas.ProductionLogResponse])
def get_logs(db: Session = Depends(get_db)):
    """Get all production logs with all related data"""
    logs = db.query(models.ProductionLog)\
        .options(
            joinedload(models.ProductionLog.worker).joinedload(models.Worker.position),
            joinedload(models.ProductionLog.worker).joinedload(models.Worker.department).joinedload(models.Department.division),
            joinedload(models.ProductionLog.position),
            joinedload(models.ProductionLog.sub_position).joinedload(models.SubPosition.position),
            joinedload(models.ProductionLog.shift),
            joinedload(models.ProductionLog.supplier),
            joinedload(models.ProductionLog.item),
            joinedload(models.ProductionLog.approved_coordinator_by_worker),
            joinedload(models.ProductionLog.approved_spv_by_worker),
            selectinload(models.ProductionLog.production_log_problem_comments).joinedload(models.ProductionLogProblemComment.problem_comment)
        )\
        .all()
    return [_format_production_log_response(log) for log in logs]


@router.get("/{log_id}", response_model=schemas.ProductionLogResponse)
def get_log(log_id: int, db: Session = Depends(get_db)):
    """Get a production log by ID with all related data"""
    log = db.query(models.ProductionLog)\
        .options(
            joinedload(models.ProductionLog.worker).joinedload(models.Worker.position),
            joinedload(models.ProductionLog.worker).joinedload(models.Worker.department).joinedload(models.Department.division),
            joinedload(models.ProductionLog.position),
            joinedload(models.ProductionLog.sub_position).joinedload(models.SubPosition.position),
            joinedload(models.ProductionLog.shift),
            joinedload(models.ProductionLog.supplier),
            joinedload(models.ProductionLog.item),
            joinedload(models.ProductionLog.approved_coordinator_by_worker),
            joinedload(models.ProductionLog.approved_spv_by_worker),
            selectinload(models.ProductionLog.production_log_problem_comments).joinedload(models.ProductionLogProblemComment.problem_comment)
        )\
        .filter(models.ProductionLog.id == log_id)\
        .first()
    if not log:
        raise HTTPException(status_code=404, detail="Production log tidak ditemukan")
    return _format_production_log_response(log)


@router.post("", response_model=schemas.ProductionLogResponse, status_code=201)
@router.post("/", response_model=schemas.ProductionLogResponse, status_code=201)
def create_log(data: schemas.ProductionLogCreate, db: Session = Depends(get_db)):
    """Create a new production log"""
    # Validate all foreign keys
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

    # Validate problem comments if provided
    problem_comment_ids = data.problem_comment_ids or []
    if problem_comment_ids:
        for pc_id in problem_comment_ids:
            if not db.query(models.ProblemComment).filter(models.ProblemComment.id == pc_id).first():
                raise HTTPException(status_code=404, detail=f"Problem comment dengan ID {pc_id} tidak ditemukan")

    # Create production log
    log_data = data.model_dump(exclude={"problem_comment_ids"})
    log = models.ProductionLog(**log_data)
    db.add(log)
    db.flush()  # Flush to get the ID

    # Create many-to-many relationships
    for pc_id in problem_comment_ids:
        plpc = models.ProductionLogProblemComment(
            production_log_id=log.id,
            problem_comment_id=pc_id
        )
        db.add(plpc)

    db.commit()
    db.refresh(log)

    # Reload with relationships
    log = db.query(models.ProductionLog)\
        .options(
            joinedload(models.ProductionLog.worker).joinedload(models.Worker.position),
            joinedload(models.ProductionLog.worker).joinedload(models.Worker.department).joinedload(models.Department.division),
            joinedload(models.ProductionLog.position),
            joinedload(models.ProductionLog.sub_position).joinedload(models.SubPosition.position),
            joinedload(models.ProductionLog.shift),
            joinedload(models.ProductionLog.supplier),
            joinedload(models.ProductionLog.item),
            joinedload(models.ProductionLog.approved_coordinator_by_worker),
            joinedload(models.ProductionLog.approved_spv_by_worker),
            selectinload(models.ProductionLog.production_log_problem_comments).joinedload(models.ProductionLogProblemComment.problem_comment)
        )\
        .filter(models.ProductionLog.id == log.id)\
        .first()
    return _format_production_log_response(log)


@router.put("/{log_id}", response_model=schemas.ProductionLogResponse)
def update_log(log_id: int, data: schemas.ProductionLogUpdate, db: Session = Depends(get_db)):
    """Update a production log"""
    log = db.query(models.ProductionLog)\
        .filter(models.ProductionLog.id == log_id)\
        .first()
    if not log:
        raise HTTPException(status_code=404, detail="Production log tidak ditemukan")
    
    # Verify foreign keys if they are being updated
    if data.worker_id is not None:
        if not db.query(models.Worker).filter(models.Worker.id == data.worker_id).first():
            raise HTTPException(status_code=404, detail="Worker tidak ditemukan")
    
    if data.position_id is not None:
        if not db.query(models.Position).filter(models.Position.id == data.position_id).first():
            raise HTTPException(status_code=404, detail="Position tidak ditemukan")
    
    if data.sub_position_id is not None:
        if not db.query(models.SubPosition).filter(models.SubPosition.id == data.sub_position_id).first():
            raise HTTPException(status_code=404, detail="Sub position tidak ditemukan")
    
    if data.shift_id is not None:
        if not db.query(models.Shift).filter(models.Shift.id == data.shift_id).first():
            raise HTTPException(status_code=404, detail="Shift tidak ditemukan")
    
    if data.supplier_id is not None:
        if not db.query(models.Supplier).filter(models.Supplier.id == data.supplier_id).first():
            raise HTTPException(status_code=404, detail="Supplier tidak ditemukan")
    
    if data.item_id is not None:
        if not db.query(models.Item).filter(models.Item.id == data.item_id).first():
            raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    if data.approved_coordinator_by is not None:
        if not db.query(models.Worker).filter(models.Worker.id == data.approved_coordinator_by).first():
            raise HTTPException(status_code=404, detail="Approver coordinator tidak ditemukan")
    
    if data.approved_spv_by is not None:
        if not db.query(models.Worker).filter(models.Worker.id == data.approved_spv_by).first():
            raise HTTPException(status_code=404, detail="Approver SPV tidak ditemukan")

    # Validate problem comments if provided
    problem_comment_ids = data.problem_comment_ids
    if problem_comment_ids is not None:
        for pc_id in problem_comment_ids:
            if not db.query(models.ProblemComment).filter(models.ProblemComment.id == pc_id).first():
                raise HTTPException(status_code=404, detail=f"Problem comment dengan ID {pc_id} tidak ditemukan")

    # Update basic fields
    update_data = data.model_dump(exclude_unset=True, exclude={"problem_comment_ids"})
    
    # Handle approval timestamps
    if data.approved_coordinator is not None:
        if data.approved_coordinator and log.approved_coordinator_at is None:
            update_data["approved_coordinator_at"] = datetime.now()
        elif not data.approved_coordinator:
            update_data["approved_coordinator_at"] = None
    
    if data.approved_spv is not None:
        if data.approved_spv and log.approved_spv_at is None:
            update_data["approved_spv_at"] = datetime.now()
        elif not data.approved_spv:
            update_data["approved_spv_at"] = None

    for field, value in update_data.items():
        setattr(log, field, value)
    
    # Update many-to-many relationships if provided
    if problem_comment_ids is not None:
        # Delete existing relationships
        db.query(models.ProductionLogProblemComment)\
            .filter(models.ProductionLogProblemComment.production_log_id == log_id)\
            .delete()
        
        # Create new relationships
        for pc_id in problem_comment_ids:
            plpc = models.ProductionLogProblemComment(
                production_log_id=log.id,
                problem_comment_id=pc_id
            )
            db.add(plpc)
    
    db.commit()
    db.refresh(log)

    # Reload with relationships
    log = db.query(models.ProductionLog)\
        .options(
            joinedload(models.ProductionLog.worker).joinedload(models.Worker.position),
            joinedload(models.ProductionLog.worker).joinedload(models.Worker.department).joinedload(models.Department.division),
            joinedload(models.ProductionLog.position),
            joinedload(models.ProductionLog.sub_position).joinedload(models.SubPosition.position),
            joinedload(models.ProductionLog.shift),
            joinedload(models.ProductionLog.supplier),
            joinedload(models.ProductionLog.item),
            joinedload(models.ProductionLog.approved_coordinator_by_worker),
            joinedload(models.ProductionLog.approved_spv_by_worker),
            selectinload(models.ProductionLog.production_log_problem_comments).joinedload(models.ProductionLogProblemComment.problem_comment)
        )\
        .filter(models.ProductionLog.id == log.id)\
        .first()
    return _format_production_log_response(log)


@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    """Delete a production log"""
    log = db.query(models.ProductionLog)\
        .filter(models.ProductionLog.id == log_id)\
        .first()
    if not log:
        raise HTTPException(status_code=404, detail="Production log tidak ditemukan")
    
    db.delete(log)
    db.commit()
    return {"message": "Production log berhasil dihapus"}
