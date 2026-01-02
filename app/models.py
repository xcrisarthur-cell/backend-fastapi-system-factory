from sqlalchemy import (
    Column, Integer, String, ForeignKey, BigInteger,
    Numeric, CheckConstraint, TIMESTAMP, Boolean, Text, Enum, Date, Time
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class AttendanceStatus(str, enum.Enum):
    HADIR = "HADIR"
    IJIN = "IJIN"
    CUTI = "CUTI"
    ALPA = "ALPA"

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    notes = Column(Text, nullable=True)
    approved_coordinator = Column(Boolean, default=False, nullable=True)
    approved_supervisor = Column(Boolean, default=False, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    worker = relationship("Worker", back_populates="attendances")

class Division(Base):
    __tablename__ = "divisions"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)

    # Relationships
    departments = relationship("Department", back_populates="division", cascade="all, delete-orphan")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    division_id = Column(Integer, ForeignKey("divisions.id", ondelete="RESTRICT"), nullable=False)
    code = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)

    # Relationships
    division = relationship("Division", back_populates="departments")
    workers = relationship("Worker", back_populates="department", cascade="all, delete-orphan")

    __table_args__ = (
        {"extend_existing": True}
    )


class ProductionTarget(Base):
    __tablename__ = "production_targets"

    id = Column(Integer, primary_key=True)
    target = Column(Numeric(10, 2), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="SET NULL"), nullable=True)
    sub_position_id = Column(Integer, ForeignKey("sub_positions.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    position = relationship("Position", back_populates="production_targets", foreign_keys=[position_id])
    sub_position = relationship("SubPosition", back_populates="production_targets", foreign_keys=[sub_position_id])


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(50), nullable=True)
    unit = Column(String(10), nullable=False)

    # Relationships
    production_targets = relationship("ProductionTarget", back_populates="position")
    sub_positions = relationship("SubPosition", back_populates="position", cascade="all, delete-orphan")
    workers = relationship("Worker", back_populates="position", cascade="all, delete-orphan")
    production_logs = relationship("ProductionLog", back_populates="position", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("unit IN ('pcs', 'lmbr')", name="positions_unit_check"),
        {"extend_existing": True}
    )


class SubPosition(Base):
    __tablename__ = "sub_positions"

    id = Column(Integer, primary_key=True)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="RESTRICT"), nullable=False)
    code = Column(String(30), nullable=False)

    # Relationships
    production_targets = relationship("ProductionTarget", back_populates="sub_position")
    position = relationship("Position", back_populates="sub_positions")
    production_logs = relationship("ProductionLog", back_populates="sub_position", cascade="all, delete-orphan")

    __table_args__ = (
        {"extend_existing": True}
    )


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="RESTRICT"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="RESTRICT"), nullable=True)

    # Relationships
    position = relationship("Position", back_populates="workers")
    department = relationship("Department", back_populates="workers")
    production_logs = relationship("ProductionLog", back_populates="worker", foreign_keys="ProductionLog.worker_id", cascade="all, delete-orphan")
    approved_coordinator_logs = relationship("ProductionLog", back_populates="approved_coordinator_by_worker", foreign_keys="ProductionLog.approved_coordinator_by", cascade="all, delete-orphan")
    approved_spv_logs = relationship("ProductionLog", back_populates="approved_spv_by_worker", foreign_keys="ProductionLog.approved_spv_by", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="worker", cascade="all, delete-orphan")

    __table_args__ = (
        {"extend_existing": True}
    )


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    # Relationships
    production_logs = relationship("ProductionLog", back_populates="shift", cascade="all, delete-orphan")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relationships
    production_logs = relationship("ProductionLog", back_populates="supplier", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    item_number = Column(String(50), unique=True, nullable=False)
    item_name = Column(String(100), nullable=True)
    spec = Column(Text, nullable=True)

    # Relationships
    production_logs = relationship("ProductionLog", back_populates="item", cascade="all, delete-orphan")


class ProblemComment(Base):
    __tablename__ = "problem_comments"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), unique=True, nullable=False)

    # Relationships
    production_log_problem_comments = relationship("ProductionLogProblemComment", back_populates="problem_comment", cascade="all, delete-orphan")


class ProductionLog(Base):
    __tablename__ = "production_logs"

    id = Column(BigInteger, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    sub_position_id = Column(Integer, ForeignKey("sub_positions.id"), nullable=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    qty_output = Column(Numeric(10, 2), nullable=False)
    qty_reject = Column(Numeric(10, 2), nullable=False)
    problem_duration_minutes = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    approved_coordinator = Column(Boolean, nullable=True)
    approved_spv = Column(Boolean, nullable=True)
    approved_coordinator_at = Column(TIMESTAMP, nullable=True)
    approved_spv_at = Column(TIMESTAMP, nullable=True)
    approved_coordinator_by = Column(Integer, ForeignKey("workers.id"), nullable=True)
    approved_spv_by = Column(Integer, ForeignKey("workers.id"), nullable=True)

    # Relationships
    worker = relationship("Worker", back_populates="production_logs", foreign_keys=[worker_id])
    position = relationship("Position", back_populates="production_logs")
    sub_position = relationship("SubPosition", back_populates="production_logs")
    shift = relationship("Shift", back_populates="production_logs")
    supplier = relationship("Supplier", back_populates="production_logs")
    item = relationship("Item", back_populates="production_logs")
    approved_coordinator_by_worker = relationship("Worker", back_populates="approved_coordinator_logs", foreign_keys=[approved_coordinator_by])
    approved_spv_by_worker = relationship("Worker", back_populates="approved_spv_logs", foreign_keys=[approved_spv_by])
    production_log_problem_comments = relationship("ProductionLogProblemComment", back_populates="production_log", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("problem_duration_minutes >= 0", name="production_logs_problem_duration_minutes_check"),
        CheckConstraint("qty_output >= 0", name="production_logs_qty_output_check"),
        CheckConstraint("qty_reject >= 0", name="production_logs_qty_reject_check"),
        CheckConstraint("(approved_spv IS NULL) OR (approved_coordinator = true)", name="spv_after_coordinator_check"),
        {"extend_existing": True}
    )


class ProductionLogProblemComment(Base):
    __tablename__ = "production_log_problem_comments"

    id = Column(Integer, primary_key=True)
    production_log_id = Column(BigInteger, ForeignKey("production_logs.id", ondelete="CASCADE"), nullable=False)
    problem_comment_id = Column(Integer, ForeignKey("problem_comments.id", ondelete="RESTRICT"), nullable=False)

    # Relationships
    production_log = relationship("ProductionLog", back_populates="production_log_problem_comments")
    problem_comment = relationship("ProblemComment", back_populates="production_log_problem_comments")

    __table_args__ = (
        {"extend_existing": True}
    )
