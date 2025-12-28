from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ========= DIVISION =========
class DivisionCreate(BaseModel):
    code: str
    name: str


class DivisionUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None


class DivisionResponse(DivisionCreate):
    id: int

    class Config:
        from_attributes = True


# ========= DEPARTMENT =========
class DepartmentCreate(BaseModel):
    division_id: int
    code: str
    name: str


class DepartmentUpdate(BaseModel):
    division_id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None


class DepartmentResponse(DepartmentCreate):
    id: int
    division: Optional[DivisionResponse] = None

    class Config:
        from_attributes = True


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
    position: Optional[PositionResponse] = None

    class Config:
        from_attributes = True


# ========= WORKER =========
class WorkerCreate(BaseModel):
    name: str
    password: Optional[str] = None
    position_id: Optional[int] = None
    department_id: Optional[int] = None


class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    position_id: Optional[int] = None
    department_id: Optional[int] = None


class WorkerResponse(BaseModel):
    id: int
    name: str
    position_id: Optional[int] = None
    department_id: Optional[int] = None
    position: Optional[PositionResponse] = None
    department: Optional[DepartmentResponse] = None
    # Note: password is excluded from response for security

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


# ========= PRODUCTION LOG PROBLEM COMMENT =========
class ProductionLogProblemCommentCreate(BaseModel):
    production_log_id: int
    problem_comment_id: int


class ProductionLogProblemCommentResponse(ProductionLogProblemCommentCreate):
    id: int
    problem_comment: Optional[ProblemCommentResponse] = None

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
    problem_duration_minutes: Optional[int] = None
    problem_comment_ids: Optional[List[int]] = None  # For many-to-many relationship


class ProductionLogUpdate(BaseModel):
    worker_id: Optional[int] = None
    position_id: Optional[int] = None
    sub_position_id: Optional[int] = None
    shift_id: Optional[int] = None
    supplier_id: Optional[int] = None
    item_id: Optional[int] = None
    qty_output: Optional[float] = None
    qty_reject: Optional[float] = None
    problem_duration_minutes: Optional[int] = None
    problem_comment_ids: Optional[List[int]] = None
    approved_coordinator: Optional[bool] = None
    approved_spv: Optional[bool] = None
    approved_coordinator_by: Optional[int] = None
    approved_spv_by: Optional[int] = None


class ProductionLogResponse(BaseModel):
    id: int
    worker_id: int
    position_id: int
    sub_position_id: Optional[int] = None
    shift_id: int
    supplier_id: Optional[int] = None
    item_id: int
    qty_output: float
    qty_reject: float
    problem_duration_minutes: Optional[int] = None
    created_at: datetime
    approved_coordinator: Optional[bool] = None
    approved_spv: Optional[bool] = None
    approved_coordinator_at: Optional[datetime] = None
    approved_spv_at: Optional[datetime] = None
    approved_coordinator_by: Optional[int] = None
    approved_spv_by: Optional[int] = None
    # Nested relationships
    worker: Optional[WorkerResponse] = None
    position: Optional[PositionResponse] = None
    sub_position: Optional[SubPositionResponse] = None
    shift: Optional[ShiftResponse] = None
    supplier: Optional[SupplierResponse] = None
    item: Optional[ItemResponse] = None
    approved_coordinator_by_worker: Optional[WorkerResponse] = None
    approved_spv_by_worker: Optional[WorkerResponse] = None
    problem_comments: Optional[List[ProblemCommentResponse]] = None

    class Config:
        from_attributes = True
