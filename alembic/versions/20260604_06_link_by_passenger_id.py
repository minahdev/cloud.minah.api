"""link person and booking by passenger_id only (drop id, booking_id)

Revision ID: 20260604_06
Revises: 20260604_05
Create Date: 2026-06-04

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "20260604_06"
down_revision: Union[str, Sequence[str], None] = "20260604_05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _insp():
    return inspect(op.get_bind())


def upgrade() -> None:
    insp = _insp()
    person_cols = {c["name"] for c in insp.get_columns("titanic_person")}
    booking_cols = {c["name"] for c in insp.get_columns("titanic_booking")}

    if "booking_id" in person_cols:
        op.execute(
            """
            UPDATE titanic_booking AS b
            SET passenger_id = p.passenger_id
            FROM titanic_person AS p
            WHERE p.booking_id = b.id AND b.passenger_id IS NULL
            """
        )
        try:
            op.drop_constraint("uq_titanic_person_booking_id", "titanic_person", type_="unique")
        except Exception:
            pass
        try:
            op.drop_constraint("fk_titanic_person_booking_id", "titanic_person", type_="foreignkey")
        except Exception:
            pass
        op.drop_column("titanic_person", "booking_id")

    if "passenger_id" not in booking_cols:
        op.add_column(
            "titanic_booking",
            sa.Column("passenger_id", sa.String(length=32), nullable=True),
        )
        booking_cols.add("passenger_id")

    if "booking_id" in person_cols and "id" in booking_cols:
        op.execute(
            """
            UPDATE titanic_booking AS b
            SET passenger_id = p.passenger_id
            FROM titanic_person AS p
            WHERE p.booking_id = b.id AND (b.passenger_id IS NULL OR b.passenger_id = '')
            """
        )

    op.alter_column("titanic_booking", "passenger_id", nullable=False)

    if "id" in booking_cols:
        try:
            op.drop_constraint("titanic_booking_pkey", "titanic_booking", type_="primary")
        except Exception:
            pass
        op.drop_column("titanic_booking", "id")
        op.create_primary_key("titanic_booking_pkey", "titanic_booking", ["passenger_id"])

    fks = {fk["name"] for fk in insp.get_foreign_keys("titanic_booking")}
    if "titanic_booking_passenger_id_fkey" not in fks:
        op.create_foreign_key(
            "titanic_booking_passenger_id_fkey",
            "titanic_booking",
            "titanic_person",
            ["passenger_id"],
            ["passenger_id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    pass
