from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from app.database import get_db
from app import models, schemas
from app.security import hash_password, verify_password

router = APIRouter(prefix="/workers", tags=["Workers"])


class WorkerLogin(BaseModel):
    worker_id: int
    password: str


@router.post("/login", response_model=schemas.WorkerResponse)
def login_worker(login_data: WorkerLogin, db: Session = Depends(get_db)):
    """Login worker by verifying password"""
    worker = db.query(models.Worker)\
        .options(
            joinedload(models.Worker.position),
            joinedload(models.Worker.department).joinedload(models.Department.division)
        )\
        .filter(models.Worker.id == login_data.worker_id)\
        .first()
    
    if not worker:
        raise HTTPException(status_code=404, detail="Worker tidak ditemukan")
    
    if not worker.password:
        raise HTTPException(status_code=400, detail="Worker tidak memiliki password")
    
    # Verify password
    if not verify_password(login_data.password, worker.password):
        raise HTTPException(status_code=401, detail="Password salah")
    
    return worker


@router.get("", response_model=list[schemas.WorkerResponse])
@router.get("/", response_model=list[schemas.WorkerResponse])
def get_workers(db: Session = Depends(get_db)):
    """Get all workers with their position and department information"""
    return db.query(models.Worker)\
        .options(
            joinedload(models.Worker.position),
            joinedload(models.Worker.department).joinedload(models.Department.division)
        )\
        .all()


@router.get("/{worker_id}", response_model=schemas.WorkerResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    """Get a worker by ID with their position and department information"""
    worker = db.query(models.Worker)\
        .options(
            joinedload(models.Worker.position),
            joinedload(models.Worker.department).joinedload(models.Department.division)
        )\
        .filter(models.Worker.id == worker_id)\
        .first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker tidak ditemukan")
    return worker


@router.post("/", response_model=schemas.WorkerResponse, status_code=201)
def create_worker(data: schemas.WorkerCreate, db: Session = Depends(get_db)):
    """Create a new worker"""
    try:
        # Validate position exists if provided
        if data.position_id is not None:
            position = db.query(models.Position).filter(models.Position.id == data.position_id).first()
            if not position:
                raise HTTPException(status_code=404, detail="Position tidak ditemukan")
        
        # Validate department exists if provided
        if data.department_id is not None:
            department = db.query(models.Department).filter(models.Department.id == data.department_id).first()
            if not department:
                raise HTTPException(status_code=404, detail="Department tidak ditemukan")
        
        # Prepare worker data
        worker_data = data.model_dump()
        
        # Hash password if provided
        if worker_data.get('password'):
            plain_password = worker_data['password']
            # print("=" * 60)
            # print("CREATE WORKER - PASSWORD LOGGING")
            # print("=" * 60)
            # print(f"[BEFORE HASH] Password (plain text): {plain_password}")
            
            try:
                hashed_password = hash_password(plain_password)
                worker_data['password'] = hashed_password
                print(f"[AFTER HASH]  Password (hashed):   {hashed_password}")
                print("=" * 60)
            except Exception as e:
                print(f"[ERROR] Failed to hash password: {str(e)}")
                print("=" * 60)
                raise HTTPException(status_code=500, detail=f"Error hashing password: {str(e)}")
        
        worker = models.Worker(**worker_data)
        db.add(worker)
        db.commit()
        db.refresh(worker)
        
        # Log password stored in database
        if worker.password:
            print(f"[STORED IN DB] Password (hashed):   {worker.password}")
            print(f"[WORKER ID]   Created worker ID:    {worker.id}")
            print("=" * 60)
        
        # Reload with relationships
        return db.query(models.Worker)\
            .options(
                joinedload(models.Worker.position),
                joinedload(models.Worker.department).joinedload(models.Department.division)
            )\
            .filter(models.Worker.id == worker.id)\
            .first()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating worker: {str(e)}")


@router.put("/{worker_id}", response_model=schemas.WorkerResponse)
def update_worker(worker_id: int, data: schemas.WorkerUpdate, db: Session = Depends(get_db)):
    """Update a worker"""
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
    
    # Validate department exists if department_id is being updated
    if data.department_id is not None:
        department = db.query(models.Department).filter(models.Department.id == data.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department tidak ditemukan")
    
    update_data = data.model_dump(exclude_unset=True)
    
    # Hash password if it's being updated
    if 'password' in update_data and update_data['password']:
        plain_password = update_data['password']
        # print("=" * 60)
        # print(f"UPDATE WORKER (ID: {worker_id}) - PASSWORD LOGGING")
        # print("=" * 60)
        # print(f"[BEFORE HASH] Password (plain text): {plain_password}")
        
        hashed_password = hash_password(plain_password)
        update_data['password'] = hashed_password
        print(f"[AFTER HASH]  Password (hashed):   {hashed_password}")
        print("=" * 60)
    
    for field, value in update_data.items():
        setattr(worker, field, value)
    
    db.commit()
    db.refresh(worker)
    
    # Log password stored in database after update
    if 'password' in update_data:
        print(f"[STORED IN DB] Password (hashed):   {worker.password}")
        print(f"[WORKER ID]   Updated worker ID:    {worker.id}")
        print("=" * 60)
    
    # Reload with relationships
    return db.query(models.Worker)\
        .options(
            joinedload(models.Worker.position),
            joinedload(models.Worker.department).joinedload(models.Department.division)
        )\
        .filter(models.Worker.id == worker.id)\
        .first()


@router.delete("/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    """Delete a worker"""
    worker = db.query(models.Worker)\
        .filter(models.Worker.id == worker_id)\
        .first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker tidak ditemukan")
    
    db.delete(worker)
    db.commit()
    return {"message": "Worker berhasil dihapus"}
