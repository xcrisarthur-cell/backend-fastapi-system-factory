from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app import models, schemas
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/production-plans", tags=["Production Plans"])


@router.get("", response_model=list[schemas.ProductionPlanResponse])
@router.get("/", response_model=list[schemas.ProductionPlanResponse])
def get_production_plans(
    worker_id: int | None = Query(default=None),
    created_by: int | None = Query(default=None),
    item_id: int | None = Query(default=None),
    position_id: int | None = Query(default=None),
    shift_id: int | None = Query(default=None),
    sub_position_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(models.ProductionPlan).options(
            joinedload(models.ProductionPlan.item),
            joinedload(models.ProductionPlan.worker),
            joinedload(models.ProductionPlan.position),
            joinedload(models.ProductionPlan.shift),
            joinedload(models.ProductionPlan.sub_position),
            joinedload(models.ProductionPlan.created_by_worker),
        )

        if worker_id is not None:
            query = query.filter(models.ProductionPlan.worker_id == worker_id)
        if created_by is not None:
            query = query.filter(models.ProductionPlan.created_by == created_by)
        if item_id is not None:
            query = query.filter(models.ProductionPlan.item_id == item_id)
        if position_id is not None:
            query = query.filter(models.ProductionPlan.position_id == position_id)
        if shift_id is not None:
            query = query.filter(models.ProductionPlan.shift_id == shift_id)
        if sub_position_id is not None:
            query = query.filter(models.ProductionPlan.sub_position_id == sub_position_id)

        return query.order_by(models.ProductionPlan.created_at.desc()).all()
    except Exception as e:
        logger.error(f"Error fetching production plans: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/{plan_id}", response_model=schemas.ProductionPlanResponse)
@router.get("/{plan_id}/", response_model=schemas.ProductionPlanResponse)
def get_production_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = (
        db.query(models.ProductionPlan)
        .options(
            joinedload(models.ProductionPlan.item),
            joinedload(models.ProductionPlan.worker),
            joinedload(models.ProductionPlan.position),
            joinedload(models.ProductionPlan.shift),
            joinedload(models.ProductionPlan.sub_position),
            joinedload(models.ProductionPlan.created_by_worker),
        )
        .filter(models.ProductionPlan.id == plan_id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Production Plan tidak ditemukan")
    return plan


@router.post("", response_model=schemas.ProductionPlanResponse, status_code=201)
@router.post("/", response_model=schemas.ProductionPlanResponse, status_code=201)
def create_production_plan(data: schemas.ProductionPlanCreate, db: Session = Depends(get_db)):
    try:
        item = db.query(models.Item).filter(models.Item.id == data.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item tidak ditemukan")

        worker = db.query(models.Worker).filter(models.Worker.id == data.worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker tidak ditemukan")

        shift = db.query(models.Shift).filter(models.Shift.id == data.shift_id).first()
        if not shift:
            raise HTTPException(status_code=404, detail="Shift tidak ditemukan")

        position = None
        if data.position_id is not None:
            position = db.query(models.Position).filter(models.Position.id == data.position_id).first()
            if not position:
                raise HTTPException(status_code=404, detail="Position tidak ditemukan")

        sub_position = None
        if data.sub_position_id is not None:
            sub_position = (
                db.query(models.SubPosition).filter(models.SubPosition.id == data.sub_position_id).first()
            )
            if not sub_position:
                raise HTTPException(status_code=404, detail="Sub Position tidak ditemukan")

        if position is not None and sub_position is not None and sub_position.position_id != position.id:
            raise HTTPException(status_code=400, detail="Sub Position tidak sesuai dengan Position")

        creator = db.query(models.Worker).filter(models.Worker.id == data.created_by).first()
        if not creator:
            raise HTTPException(status_code=404, detail="Created by worker tidak ditemukan")

        plan_data = data.model_dump()
        if plan_data.get("created_at") is None:
            del plan_data["created_at"]

        plan = models.ProductionPlan(**plan_data)
        db.add(plan)
        db.commit()
        db.refresh(plan)

        return (
            db.query(models.ProductionPlan)
            .options(
                joinedload(models.ProductionPlan.item),
                joinedload(models.ProductionPlan.worker),
                joinedload(models.ProductionPlan.position),
                joinedload(models.ProductionPlan.shift),
                joinedload(models.ProductionPlan.sub_position),
                joinedload(models.ProductionPlan.created_by_worker),
            )
            .filter(models.ProductionPlan.id == plan.id)
            .first()
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating production plan: {str(e)}")


@router.put("/{plan_id}", response_model=schemas.ProductionPlanResponse)
@router.put("/{plan_id}/", response_model=schemas.ProductionPlanResponse)
def update_production_plan(plan_id: int, data: schemas.ProductionPlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(models.ProductionPlan).filter(models.ProductionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Production Plan tidak ditemukan")

    if data.item_id is not None:
        item = db.query(models.Item).filter(models.Item.id == data.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    if data.worker_id is not None:
        worker = db.query(models.Worker).filter(models.Worker.id == data.worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker tidak ditemukan")

    position = None
    if data.position_id is not None:
        position = db.query(models.Position).filter(models.Position.id == data.position_id).first()
        if not position:
            raise HTTPException(status_code=404, detail="Position tidak ditemukan")

    if data.shift_id is not None:
        shift = db.query(models.Shift).filter(models.Shift.id == data.shift_id).first()
        if not shift:
            raise HTTPException(status_code=404, detail="Shift tidak ditemukan")

    sub_position = None
    if data.sub_position_id is not None:
        sub_position = (
            db.query(models.SubPosition).filter(models.SubPosition.id == data.sub_position_id).first()
        )
        if not sub_position:
            raise HTTPException(status_code=404, detail="Sub Position tidak ditemukan")

    effective_position_id = data.position_id if "position_id" in data.model_fields_set else plan.position_id
    effective_sub_position_id = (
        data.sub_position_id if "sub_position_id" in data.model_fields_set else plan.sub_position_id
    )

    if effective_position_id is not None and effective_sub_position_id is not None:
        if sub_position is None:
            sub_position = (
                db.query(models.SubPosition).filter(models.SubPosition.id == effective_sub_position_id).first()
            )
            if not sub_position:
                raise HTTPException(status_code=404, detail="Sub Position tidak ditemukan")
        if sub_position.position_id != effective_position_id:
            raise HTTPException(status_code=400, detail="Sub Position tidak sesuai dengan Position")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)

    try:
        db.commit()
        db.refresh(plan)
        return (
            db.query(models.ProductionPlan)
            .options(
                joinedload(models.ProductionPlan.item),
                joinedload(models.ProductionPlan.worker),
                joinedload(models.ProductionPlan.position),
                joinedload(models.ProductionPlan.shift),
                joinedload(models.ProductionPlan.sub_position),
                joinedload(models.ProductionPlan.created_by_worker),
            )
            .filter(models.ProductionPlan.id == plan.id)
            .first()
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating production plan: {str(e)}")


@router.delete("/{plan_id}")
@router.delete("/{plan_id}/")
def delete_production_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(models.ProductionPlan).filter(models.ProductionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Production Plan tidak ditemukan")

    try:
        db.delete(plan)
        db.commit()
        return {"message": "Production Plan berhasil dihapus"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting production plan: {str(e)}")
