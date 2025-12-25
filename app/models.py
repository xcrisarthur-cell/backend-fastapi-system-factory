from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    Numeric, CheckConstraint, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    unit = Column(String(10), nullable=False)

class SubPosition(Base):
    __tablename__ = "sub_positions"

    id = Column(Integer, primary_key=True)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="RESTRICT"))
    code = Column(String(30), nullable=False)

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="RESTRICT"), nullable=False)

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    item_number = Column(String(50), unique=True, nullable=False)
    item_name = Column(String(100))
    spec = Column(String)

class ProblemComment(Base):
    __tablename__ = "problem_comments"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), unique=True, nullable=False)

class ProductionLog(Base):
    __tablename__ = "production_logs"

    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    sub_position_id = Column(Integer, ForeignKey("sub_positions.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    item_id = Column(Integer, ForeignKey("items.id"))

    qty_output = Column(Numeric(10, 2), nullable=False)
    qty_reject = Column(Numeric(10, 2), nullable=False)

    problem_comment_id = Column(Integer, ForeignKey("problem_comments.id"), nullable=True)
    problem_duration_minutes = Column(Integer, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
