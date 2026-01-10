"""fix_production_plan_position_id_and_nullable_sub_position

Revision ID: 2a23bf950eb4
Revises: a75499d5f54b
Create Date: 2026-01-09 14:08:48.983393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a23bf950eb4'
down_revision: Union[str, None] = 'a75499d5f54b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("production_plan", schema="public"):
        return

    columns = {col["name"]: col for col in inspector.get_columns("production_plan", schema="public")}

    if "position_id" not in columns:
        op.add_column("production_plan", sa.Column("position_id", sa.Integer(), nullable=True), schema="public")
        op.create_foreign_key(
            None,
            "production_plan",
            "positions",
            ["position_id"],
            ["id"],
            source_schema="public",
            referent_schema="public",
            ondelete="RESTRICT",
        )

    sub_position = columns.get("sub_position_id")
    if sub_position and sub_position.get("nullable") is False:
        op.alter_column(
            "production_plan",
            "sub_position_id",
            existing_type=sa.Integer(),
            nullable=True,
            schema="public",
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("production_plan", schema="public"):
        return

    columns = {col["name"]: col for col in inspector.get_columns("production_plan", schema="public")}

    sub_position = columns.get("sub_position_id")
    if sub_position and sub_position.get("nullable") is True:
        op.alter_column(
            "production_plan",
            "sub_position_id",
            existing_type=sa.Integer(),
            nullable=False,
            schema="public",
        )

    if "position_id" in columns:
        for fk in inspector.get_foreign_keys("production_plan", schema="public"):
            if fk.get("constrained_columns") == ["position_id"] and fk.get("referred_table") == "positions":
                fk_name = fk.get("name")
                if fk_name:
                    op.drop_constraint(fk_name, "production_plan", type_="foreignkey", schema="public")
                break
        op.drop_column("production_plan", "position_id", schema="public")

