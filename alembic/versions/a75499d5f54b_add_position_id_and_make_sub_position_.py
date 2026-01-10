"""add_position_id_and_make_sub_position_nullable_on_production_plan

Revision ID: a75499d5f54b
Revises: 6470de321ba2
Create Date: 2026-01-09 14:05:23.509340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a75499d5f54b'
down_revision: Union[str, None] = '6470de321ba2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table("production_plan"):
        columns = {col["name"] for col in inspector.get_columns("production_plan")}
        if "position_id" not in columns:
            op.add_column("production_plan", sa.Column("position_id", sa.Integer(), nullable=True))
            op.create_foreign_key(
                None,
                "production_plan",
                "positions",
                ["position_id"],
                ["id"],
                ondelete="RESTRICT",
            )

        if "sub_position_id" in columns:
            op.alter_column("production_plan", "sub_position_id", existing_type=sa.Integer(), nullable=True)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table("production_plan"):
        columns = {col["name"] for col in inspector.get_columns("production_plan")}
        if "sub_position_id" in columns:
            op.alter_column("production_plan", "sub_position_id", existing_type=sa.Integer(), nullable=False)

        if "position_id" in columns:
            for fk in inspector.get_foreign_keys("production_plan"):
                if fk.get("constrained_columns") == ["position_id"] and fk.get("referred_table") == "positions":
                    fk_name = fk.get("name")
                    if fk_name:
                        op.drop_constraint(fk_name, "production_plan", type_="foreignkey")
                    break
            op.drop_column("production_plan", "position_id")

