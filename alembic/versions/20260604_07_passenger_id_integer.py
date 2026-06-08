"""passenger_id varchar -> integer

Revision ID: 20260604_07
Revises: 20260604_06
Create Date: 2026-06-04

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260604_07"
down_revision: Union[str, Sequence[str], None] = "20260604_06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE titanic_booking DROP CONSTRAINT IF EXISTS titanic_booking_passenger_id_fkey"
    )
    op.execute(
        """
        ALTER TABLE titanic_person
        ALTER COLUMN passenger_id TYPE INTEGER
        USING passenger_id::integer
        """
    )
    op.execute(
        """
        ALTER TABLE titanic_booking
        ALTER COLUMN passenger_id TYPE INTEGER
        USING passenger_id::integer
        """
    )
    op.create_foreign_key(
        "titanic_booking_passenger_id_fkey",
        "titanic_booking",
        "titanic_person",
        ["passenger_id"],
        ["passenger_id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE titanic_booking DROP CONSTRAINT IF EXISTS titanic_booking_passenger_id_fkey"
    )
    op.execute(
        """
        ALTER TABLE titanic_booking
        ALTER COLUMN passenger_id TYPE VARCHAR(32)
        USING passenger_id::text
        """
    )
    op.execute(
        """
        ALTER TABLE titanic_person
        ALTER COLUMN passenger_id TYPE VARCHAR(32)
        USING passenger_id::text
        """
    )
    op.create_foreign_key(
        "titanic_booking_passenger_id_fkey",
        "titanic_booking",
        "titanic_person",
        ["passenger_id"],
        ["passenger_id"],
        ondelete="CASCADE",
    )
