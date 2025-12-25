from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ========= POSITION =========
class PositionCreate(BaseModel):
    code: str
    unit: str

class PositionUpdate(BaseModel):
    code: Optional[str] = None
    unit: Optional[str] = None

class PositionResponse(PositionCreate):
    id: int
    class Config:
        from_attributes = True


# ========= SUB POSITION =========
class SubPositionCreate(BaseModel):
    position_id: int
    code: str

class SubPositionUpdate(BaseModel):
    position_id: Optional[int] = None
    code: Optional[str] = None

class SubPositionResponse(SubPositionCreate):
    id: int
    class Config:
        from_attributes = True


# ========= WORKER =========
class WorkerCreate(BaseModel):
    name: str
    position_id: int

class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    position_id: Optional[int] = None

class WorkerResponse(WorkerCreate):
    id: int
    class Config:
        from_attributes = True


# ========= SHIFT =========
class ShiftCreate(BaseModel):
    name: str

class ShiftUpdate(BaseModel):
    name: Optional[str] = None

class ShiftResponse(ShiftCreate):
    id: int
    class Config:
        from_attributes = True


# ========= SUPPLIER =========
class SupplierCreate(BaseModel):
    name: str

class SupplierUpdate(BaseModel):
    name: Optional[str] = None

class SupplierResponse(SupplierCreate):
    id: int
    class Config:
        from_attributes = True


# ========= ITEM =========
class ItemCreate(BaseModel):
    item_number: str
    item_name: Optional[str] = None
    spec: Optional[str] = None

class ItemUpdate(BaseModel):
    item_number: Optional[str] = None
    item_name: Optional[str] = None
    spec: Optional[str] = None

class ItemResponse(ItemCreate):
    id: int
    class Config:
        from_attributes = True


# ========= PROBLEM COMMENT =========
class ProblemCommentCreate(BaseModel):
    description: str

class ProblemCommentUpdate(BaseModel):
    description: Optional[str] = None

class ProblemCommentResponse(ProblemCommentCreate):
    id: int
    class Config:
        from_attributes = True


# ========= PRODUCTION LOG =========
class ProductionLogCreate(BaseModel):
    worker_id: int
    position_id: int
    sub_position_id: Optional[int] = None
    shift_id: int
    supplier_id: Optional[int] = None
    item_id: int
    qty_output: float
    qty_reject: float
    problem_comment_id: Optional[int] = None
    problem_duration_minutes: Optional[int] = None

class ProductionLogUpdate(BaseModel):
    worker_id: Optional[int] = None
    position_id: Optional[int] = None
    sub_position_id: Optional[int] = None
    shift_id: Optional[int] = None
    supplier_id: Optional[int] = None
    item_id: Optional[int] = None
    qty_output: Optional[float] = None
    qty_reject: Optional[float] = None
    problem_comment_id: Optional[int] = None
    problem_duration_minutes: Optional[int] = None

class ProductionLogResponse(ProductionLogCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
