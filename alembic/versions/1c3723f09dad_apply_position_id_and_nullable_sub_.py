"""apply_position_id_and_nullable_sub_position_on_production_plan

Revision ID: 1c3723f09dad
Revises: 2a23bf950eb4
Create Date: 2026-01-09 14:17:17.481151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c3723f09dad'
down_revision: Union[str, None] = '2a23bf950eb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE IF EXISTS public.production_plan ADD COLUMN IF NOT EXISTS position_id INTEGER")
    op.execute("ALTER TABLE IF EXISTS public.production_plan ALTER COLUMN sub_position_id DROP NOT NULL")
    op.execute(
        """
        DO $$
        BEGIN
          IF NOT EXISTS (
            SELECT 1
            FROM pg_constraint c
            JOIN pg_class t ON t.oid = c.conrelid
            JOIN pg_namespace n ON n.oid = t.relnamespace
            WHERE c.conname = 'fk_production_plan_position_id_positions'
              AND n.nspname = 'public'
              AND t.relname = 'production_plan'
          ) THEN
            ALTER TABLE public.production_plan
              ADD CONSTRAINT fk_production_plan_position_id_positions
              FOREIGN KEY (position_id) REFERENCES public.positions(id)
              ON DELETE RESTRICT;
          END IF;
        END $$;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
          IF EXISTS (
            SELECT 1
            FROM pg_constraint c
            JOIN pg_class t ON t.oid = c.conrelid
            JOIN pg_namespace n ON n.oid = t.relnamespace
            WHERE c.conname = 'fk_production_plan_position_id_positions'
              AND n.nspname = 'public'
              AND t.relname = 'production_plan'
          ) THEN
            ALTER TABLE public.production_plan DROP CONSTRAINT fk_production_plan_position_id_positions;
          END IF;
        END $$;
        """
    )
    op.execute("ALTER TABLE IF EXISTS public.production_plan DROP COLUMN IF EXISTS position_id")
    op.execute("ALTER TABLE IF EXISTS public.production_plan ALTER COLUMN sub_position_id SET NOT NULL")

