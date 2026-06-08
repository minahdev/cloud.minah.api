"""remove booking_id from person; link via booking.passenger_id

Revision ID: 20260604_03
Revises: 20260604_02
Create Date: 2026-06-04

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "20260604_03"
down_revision: Union[str, Sequence[str], None] = "20260604_02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_names(table: str) -> set[str]:
    bind = op.get_bind()
    return {c["name"] for c in inspect(bind).get_columns(table)}


def upgrade() -> None:
    person_cols = _column_names("titanic_person")
    booking_cols = _column_names("titanic_booking")

    if "passenger_id" not in booking_cols:
        op.add_column(
            "titanic_booking",
            sa.Column("passenger_id", sa.String(length=32), nullable=True),
        )
        if "booking_id" in person_cols:
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

    if "booking_id" in person_cols:
        op.drop_constraint("uq_titanic_person_booking_id", "titanic_person", type_="unique")
        op.drop_constraint("fk_titanic_person_booking_id", "titanic_person", type_="foreignkey")
        op.drop_column("titanic_person", "booking_id")


def downgrade() -> None:
    person_cols = _column_names("titanic_person")
    booking_cols = _column_names("titanic_booking")

    if "booking_id" not in person_cols:
        op.add_column(
            "titanic_person",
            sa.Column("booking_id", sa.Integer(), nullable=True),
        )
        if "passenger_id" in booking_cols:
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

    if "passenger_id" in booking_cols:
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
