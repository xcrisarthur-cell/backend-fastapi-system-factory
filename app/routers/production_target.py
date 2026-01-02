from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/production-targets", tags=["Production Targets"])


@router.get("", response_model=list[schemas.ProductionTargetResponse])
@router.get("/", response_model=list[schemas.ProductionTargetResponse])
def get_production_targets(db: Session = Depends(get_db)):
    """Get all production targets"""
    return db.query(models.ProductionTarget)\
        .options(
            joinedload(models.ProductionTarget.position),
            joinedload(models.ProductionTarget.sub_position)
        )\
        .all()


@router.get("/{target_id}", response_model=schemas.ProductionTargetResponse)
def get_production_target(target_id: int, db: Session = Depends(get_db)):
    """Get a production target by ID"""
    target = db.query(models.ProductionTarget)\
        .options(
            joinedload(models.ProductionTarget.position),
            joinedload(models.ProductionTarget.sub_position)
        )\
        .filter(models.ProductionTarget.id == target_id)\
        .first()
    if not target:
        raise HTTPException(status_code=404, detail="Production Target tidak ditemukan")
    return target


@router.post("/", response_model=schemas.ProductionTargetResponse, status_code=201)
def create_production_target(data: schemas.ProductionTargetCreate, db: Session = Depends(get_db)):
    """Create a new production target"""
    try:
        # Validate position exists if provided
        if data.position_id is not None:
            position = db.query(models.Position).filter(models.Position.id == data.position_id).first()
            if not position:
                raise HTTPException(status_code=404, detail="Position tidak ditemukan")
        
        # Validate sub_position exists if provided
        if data.sub_position_id is not None:
            sub_position = db.query(models.SubPosition).filter(models.SubPosition.id == data.sub_position_id).first()
            if not sub_position:
                raise HTTPException(status_code=404, detail="Sub Position tidak ditemukan")

        new_target = models.ProductionTarget(**data.model_dump())
        db.add(new_target)
        db.commit()
        db.refresh(new_target)
        
        return db.query(models.ProductionTarget)\
            .options(
                joinedload(models.ProductionTarget.position),
                joinedload(models.ProductionTarget.sub_position)
            )\
            .filter(models.ProductionTarget.id == new_target.id)\
            .first()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating production target: {str(e)}")


@router.put("/{target_id}", response_model=schemas.ProductionTargetResponse)
def update_production_target(target_id: int, data: schemas.ProductionTargetUpdate, db: Session = Depends(get_db)):
    """Update a production target"""
    target = db.query(models.ProductionTarget).filter(models.ProductionTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Production Target tidak ditemukan")
    
    # Validate position exists if provided
    if data.position_id is not None:
        position = db.query(models.Position).filter(models.Position.id == data.position_id).first()
        if not position:
            raise HTTPException(status_code=404, detail="Position tidak ditemukan")
            
    # Validate sub_position exists if provided
    if data.sub_position_id is not None:
        sub_position = db.query(models.SubPosition).filter(models.SubPosition.id == data.sub_position_id).first()
        if not sub_position:
            raise HTTPException(status_code=404, detail="Sub Position tidak ditemukan")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(target, field, value)
    
    try:
        db.commit()
        db.refresh(target)
        return db.query(models.ProductionTarget)\
            .options(
                joinedload(models.ProductionTarget.position),
                joinedload(models.ProductionTarget.sub_position)
            )\
            .filter(models.ProductionTarget.id == target.id)\
            .first()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating production target: {str(e)}")


@router.delete("/{target_id}")
def delete_production_target(target_id: int, db: Session = Depends(get_db)):
    """Delete a production target"""
    target = db.query(models.ProductionTarget).filter(models.ProductionTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Production Target tidak ditemukan")
    
    try:
        db.delete(target)
        db.commit()
        return {"message": "Production Target berhasil dihapus"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting production target: {str(e)}")
