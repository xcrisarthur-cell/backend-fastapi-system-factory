"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-12-26 08:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create sequences
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS departments_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS divisions_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS items_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS positions_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS problem_comments_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS production_log_problem_comments_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS production_logs_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 9223372036854775807
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS shifts_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS sub_positions_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS suppliers_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS workers_id_seq
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 2147483647
            START 1
            CACHE 1
            NO CYCLE;
    """)
    
    # Create divisions table
    op.create_table(
        'divisions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('name')
    )
    
    # Create items table
    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_number', sa.String(length=50), nullable=False),
        sa.Column('item_name', sa.String(length=100), nullable=True),
        sa.Column('spec', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('item_number')
    )
    
    # Create positions table
    op.create_table(
        'positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('unit', sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.CheckConstraint("unit IN ('pcs', 'lmbr')", name='positions_unit_check')
    )
    
    # Create problem_comments table
    op.create_table(
        'problem_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('description')
    )
    
    # Create shifts table
    op.create_table(
        'shifts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create suppliers table
    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create departments table
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('division_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('division_id', 'code', name='departments_division_code_unique'),
        sa.ForeignKeyConstraint(['division_id'], ['divisions.id'], ondelete='RESTRICT')
    )
    
    # Create sub_positions table
    op.create_table(
        'sub_positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('position_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('position_id', 'code', name='sub_positions_position_id_code_key'),
        sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ondelete='RESTRICT')
    )
    
    # Create workers table
    op.create_table(
        'workers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('position_id', sa.Integer(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ondelete='RESTRICT')
    )
    
    # Create production_logs table
    op.create_table(
        'production_logs',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('worker_id', sa.Integer(), nullable=False),
        sa.Column('position_id', sa.Integer(), nullable=False),
        sa.Column('sub_position_id', sa.Integer(), nullable=True),
        sa.Column('shift_id', sa.Integer(), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=True),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('qty_output', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('qty_reject', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('problem_duration_minutes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('approved_coordinator', sa.Boolean(), nullable=True),
        sa.Column('approved_spv', sa.Boolean(), nullable=True),
        sa.Column('approved_coordinator_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('approved_spv_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('approved_coordinator_by', sa.Integer(), nullable=True),
        sa.Column('approved_spv_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('problem_duration_minutes >= 0', name='production_logs_problem_duration_minutes_check'),
        sa.CheckConstraint('qty_output >= 0', name='production_logs_qty_output_check'),
        sa.CheckConstraint('qty_reject >= 0', name='production_logs_qty_reject_check'),
        sa.CheckConstraint('(approved_spv IS NULL) OR (approved_coordinator = true)', name='spv_after_coordinator_check'),
        sa.ForeignKeyConstraint(['approved_coordinator_by'], ['workers.id']),
        sa.ForeignKeyConstraint(['approved_spv_by'], ['workers.id']),
        sa.ForeignKeyConstraint(['item_id'], ['items.id']),
        sa.ForeignKeyConstraint(['position_id'], ['positions.id']),
        sa.ForeignKeyConstraint(['shift_id'], ['shifts.id']),
        sa.ForeignKeyConstraint(['sub_position_id'], ['sub_positions.id']),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id']),
        sa.ForeignKeyConstraint(['worker_id'], ['workers.id'])
    )
    
    # Create production_log_problem_comments table
    op.create_table(
        'production_log_problem_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('production_log_id', sa.BigInteger(), nullable=False),
        sa.Column('problem_comment_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('production_log_id', 'problem_comment_id', name='plpc_unique'),
        sa.ForeignKeyConstraint(['problem_comment_id'], ['problem_comments.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['production_log_id'], ['production_logs.id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('production_log_problem_comments')
    op.drop_table('production_logs')
    op.drop_table('workers')
    op.drop_table('sub_positions')
    op.drop_table('departments')
    op.drop_table('suppliers')
    op.drop_table('shifts')
    op.drop_table('problem_comments')
    op.drop_table('positions')
    op.drop_table('items')
    op.drop_table('divisions')
    
    # Drop sequences
    op.execute("DROP SEQUENCE IF EXISTS workers_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS suppliers_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS sub_positions_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS shifts_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS production_logs_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS production_log_problem_comments_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS problem_comments_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS positions_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS items_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS divisions_id_seq;")
    op.execute("DROP SEQUENCE IF EXISTS departments_id_seq;")

