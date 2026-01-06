"""Add status_completion column to production_logs

Revision ID: 002_add_status_completion
Revises: 001_initial
Create Date: 2026-01-06 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002_add_status_completion'
down_revision: Union[str, None] = 'f9848fc5ad85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('production_logs', sa.Column('status_completion', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('production_logs', 'status_completion')
