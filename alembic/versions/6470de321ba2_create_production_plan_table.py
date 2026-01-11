"""create_production_plan_table

Revision ID: 6470de321ba2
Revises: 002_add_status_completion
Create Date: 2026-01-09 13:43:12.531018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6470de321ba2'
down_revision: Union[str, None] = '002_add_status_completion'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if we are in offline mode, where inspector is not available
    # In offline mode, just emit the create table DDL
    context = op.get_context()
    # Handle older Alembic versions or unexpected context types
    is_offline = getattr(context, 'is_offline_mode', lambda: False)() or not hasattr(context, 'bind') or context.bind is None
    
    if is_offline:
        op.create_table(
            'production_plan',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('target', sa.Numeric(precision=10, scale=2), nullable=False),
            sa.Column('item_id', sa.Integer(), nullable=False),
            sa.Column('worker_id', sa.Integer(), nullable=False),
            sa.Column('shift_id', sa.Integer(), nullable=False),
            sa.Column('sub_position_id', sa.Integer(), nullable=False),
            sa.Column('note', sa.Text(), nullable=True),
            sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
            sa.Column('created_by', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['created_by'], ['workers.id'], ondelete='RESTRICT'),
            sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='RESTRICT'),
            sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ondelete='RESTRICT'),
            sa.ForeignKeyConstraint(['sub_position_id'], ['sub_positions.id'], ondelete='RESTRICT'),
            sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ondelete='RESTRICT'),
            sa.PrimaryKeyConstraint('id'),
        )
        return

    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table('production_plan'):
        op.create_table(
            'production_plan',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('target', sa.Numeric(precision=10, scale=2), nullable=False),
            sa.Column('item_id', sa.Integer(), nullable=False),
            sa.Column('worker_id', sa.Integer(), nullable=False),
            sa.Column('shift_id', sa.Integer(), nullable=False),
            sa.Column('sub_position_id', sa.Integer(), nullable=False),
            sa.Column('note', sa.Text(), nullable=True),
            sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
            sa.Column('created_by', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['created_by'], ['workers.id'], ondelete='RESTRICT'),
            sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='RESTRICT'),
            sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ondelete='RESTRICT'),
            sa.ForeignKeyConstraint(['sub_position_id'], ['sub_positions.id'], ondelete='RESTRICT'),
            sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ondelete='RESTRICT'),
            sa.PrimaryKeyConstraint('id'),
        )


def downgrade() -> None:
    # Similar check for offline mode or just drop unconditionally if safe
    context = op.get_context()
    is_offline = getattr(context, 'is_offline_mode', lambda: False)() or not hasattr(context, 'bind') or context.bind is None
    
    if is_offline:
         op.drop_table('production_plan')
         return

    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table('production_plan'):
        op.drop_table('production_plan')

