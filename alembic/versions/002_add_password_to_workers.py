"""Add password column to workers

Revision ID: 002_add_password
Revises: 001_initial
Create Date: 2024-12-26 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_add_password'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add password column to workers table
    op.add_column('workers', sa.Column('password', sa.String(length=255), nullable=True))


def downgrade() -> None:
    # Remove password column from workers table
    op.drop_column('workers', 'password')


