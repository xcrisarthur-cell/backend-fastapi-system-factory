from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/problem-comments", tags=["Problem Comments"])

@router.get("/", response_model=list[schemas.ProblemCommentResponse])
def get_comments(db: Session = Depends(get_db)):
    return db.query(models.ProblemComment).all()

@router.get("/{comment_id}", response_model=schemas.ProblemCommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.ProblemComment)\
        .filter(models.ProblemComment.id == comment_id)\
        .first()
    if not comment:
        raise HTTPException(status_code=404, detail="Problem comment tidak ditemukan")
    return comment

@router.post("/", response_model=schemas.ProblemCommentResponse)
def create_comment(data: schemas.ProblemCommentCreate, db: Session = Depends(get_db)):
    # Check if description already exists
    exists = db.query(models.ProblemComment)\
        .filter(models.ProblemComment.description == data.description)\
        .first()
    if exists:
        raise HTTPException(status_code=400, detail="Problem comment description sudah ada")
    
    comment = models.ProblemComment(**data.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.put("/{comment_id}", response_model=schemas.ProblemCommentResponse)
def update_comment(comment_id: int, data: schemas.ProblemCommentUpdate, db: Session = Depends(get_db)):
    comment = db.query(models.ProblemComment)\
        .filter(models.ProblemComment.id == comment_id)\
        .first()
    if not comment:
        raise HTTPException(status_code=404, detail="Problem comment tidak ditemukan")
    
    # Check if new description conflicts with existing
    if data.description and data.description != comment.description:
        exists = db.query(models.ProblemComment)\
            .filter(models.ProblemComment.description == data.description)\
            .first()
        if exists:
            raise HTTPException(status_code=400, detail="Problem comment description sudah ada")
    
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
    
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.ProblemComment)\
        .filter(models.ProblemComment.id == comment_id)\
        .first()
    if not comment:
        raise HTTPException(status_code=404, detail="Problem comment tidak ditemukan")
    
    db.delete(comment)
    db.commit()
    return {"message": "Problem comment berhasil dihapus"}
