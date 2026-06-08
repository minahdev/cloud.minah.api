"""booking FK on person, remove passenger_id from booking

Revision ID: 20260604_02
Revises: 20260604_01
Create Date: 2026-06-04

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260604_02"
down_revision: Union[str, Sequence[str], None] = "20260604_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "titanic_person",
        sa.Column("booking_id", sa.Integer(), nullable=True),
    )
    op.execute(
        """
        UPDATE titanic_person AS p
        SET booking_id = b.id
        FROM titanic_booking AS b
        WHERE b.passenger_id = p.passenger_id
        """
    )
    op.create_foreign_key(
        "fk_titanic_person_booking_id",
        "titanic_person",
        "titanic_booking",
        ["booking_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_unique_constraint(
        "uq_titanic_person_booking_id",
        "titanic_person",
        ["booking_id"],
    )

    op.drop_index("ix_titanic_booking_passenger_id", table_name="titanic_booking")
    op.drop_constraint(
        "titanic_booking_passenger_id_key",
        "titanic_booking",
        type_="unique",
    )
    op.drop_constraint(
        "titanic_booking_passenger_id_fkey",
        "titanic_booking",
        type_="foreignkey",
    )
    op.drop_column("titanic_booking", "passenger_id")


def downgrade() -> None:
    op.add_column(
        "titanic_booking",
        sa.Column("passenger_id", sa.String(length=32), nullable=True),
    )
    op.execute(
        """
        UPDATE titanic_booking AS b
        SET passenger_id = p.passenger_id
        FROM titanic_person AS p
        WHERE p.booking_id = b.id
        """
    )
    op.alter_column("titanic_booking", "passenger_id", nullable=False)
    op.create_foreign_key(
        "titanic_booking_passenger_id_fkey",
        "titanic_booking",
        "titanic_person",
        ["passenger_id"],
        ["passenger_id"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint(
        "titanic_booking_passenger_id_key",
        "titanic_booking",
        ["passenger_id"],
    )
    op.create_index(
        "ix_titanic_booking_passenger_id",
        "titanic_booking",
        ["passenger_id"],
    )

    op.drop_constraint("uq_titanic_person_booking_id", "titanic_person", type_="unique")
    op.drop_constraint("fk_titanic_person_booking_id", "titanic_person", type_="foreignkey")
    op.drop_column("titanic_person", "booking_id")
