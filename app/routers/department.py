from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("", response_model=list[schemas.DepartmentResponse])
@router.get("/", response_model=list[schemas.DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    """Get all departments with their division information"""
    return db.query(models.Department)\
        .options(joinedload(models.Department.division))\
        .all()


@router.get("/{department_id}", response_model=schemas.DepartmentResponse)
def get_department(department_id: int, db: Session = Depends(get_db)):
    """Get a department by ID with division information"""
    department = db.query(models.Department)\
        .options(joinedload(models.Department.division))\
        .filter(models.Department.id == department_id)\
        .first()
    if not department:
        raise HTTPException(status_code=404, detail="Department tidak ditemukan")
    return department


@router.get("/by-division/{division_id}", response_model=list[schemas.DepartmentResponse])
def get_departments_by_division(division_id: int, db: Session = Depends(get_db)):
    """Get all departments by division ID"""
    return db.query(models.Department)\
        .options(joinedload(models.Department.division))\
        .filter(models.Department.division_id == division_id)\
        .all()


@router.post("/", response_model=schemas.DepartmentResponse, status_code=201)
def create_department(data: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new department"""
    # Validate division exists
    division = db.query(models.Division)\
        .filter(models.Division.id == data.division_id)\
        .first()
    if not division:
        raise HTTPException(status_code=404, detail="Division tidak ditemukan")
    
    # Check if code already exists for this division
    exists = db.query(models.Department)\
        .filter(
            models.Department.division_id == data.division_id,
            models.Department.code == data.code
        )\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Department code sudah ada untuk division ini")

    department = models.Department(**data.model_dump())
    db.add(department)
    db.commit()
    db.refresh(department)
    
    # Reload with relationships
    return db.query(models.Department)\
        .options(joinedload(models.Department.division))\
        .filter(models.Department.id == department.id)\
        .first()


@router.put("/{department_id}", response_model=schemas.DepartmentResponse)
def update_department(department_id: int, data: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    """Update a department"""
    department = db.query(models.Department)\
        .filter(models.Department.id == department_id)\
        .first()
    if not department:
        raise HTTPException(status_code=404, detail="Department tidak ditemukan")
    
    # Validate division exists if updating
    if data.division_id is not None:
        division = db.query(models.Division)\
            .filter(models.Division.id == data.division_id)\
            .first()
        if not division:
            raise HTTPException(status_code=404, detail="Division tidak ditemukan")
    
    # Check if new code conflicts with existing
    if data.code and data.code != department.code:
        new_division_id = data.division_id if data.division_id is not None else department.division_id
        exists = db.query(models.Department)\
            .filter(
                models.Department.division_id == new_division_id,
                models.Department.code == data.code,
                models.Department.id != department_id
            )\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Department code sudah ada untuk division ini")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(department, field, value)
    
    db.commit()
    db.refresh(department)
    
    # Reload with relationships
    return db.query(models.Department)\
        .options(joinedload(models.Department.division))\
        .filter(models.Department.id == department.id)\
        .first()


@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    """Delete a department"""
    department = db.query(models.Department)\
        .filter(models.Department.id == department_id)\
        .first()
    if not department:
        raise HTTPException(status_code=404, detail="Department tidak ditemukan")
    
    db.delete(department)
    db.commit()
    return {"message": "Department berhasil dihapus"}

