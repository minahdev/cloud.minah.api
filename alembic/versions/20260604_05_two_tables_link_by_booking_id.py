"""two tables: booking.id, person.booking_id

Revision ID: 20260604_05
Revises: 20260604_04
Create Date: 2026-06-04

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "20260604_05"
down_revision: Union[str, Sequence[str], None] = "20260604_04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _inspector():
    return inspect(op.get_bind())


def upgrade() -> None:
    insp = _inspector()
    tables = set(insp.get_table_names())
    person_cols = {c["name"] for c in insp.get_columns("titanic_person")} if "titanic_person" in tables else set()

    if "titanic_booking" not in tables:
        op.create_table(
            "titanic_booking",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("pclass", sa.String(length=8), nullable=False, server_default=""),
            sa.Column("ticket", sa.String(length=64), nullable=False, server_default=""),
            sa.Column("fare", sa.String(length=32), nullable=False, server_default=""),
            sa.Column("cabin", sa.String(length=64), nullable=False, server_default=""),
            sa.Column("embarked", sa.String(length=8), nullable=False, server_default=""),
            sa.PrimaryKeyConstraint("id"),
        )
        tables.add("titanic_booking")

    booking_cols = {c["name"] for c in insp.get_columns("titanic_booking")}

    if "passenger_id" in booking_cols and "booking_id" in person_cols:
        op.execute(
            """
            UPDATE titanic_person AS p
            SET booking_id = b.id
            FROM titanic_booking AS b
            WHERE b.passenger_id = p.passenger_id
            """
        )

    if "pclass" in person_cols:
        op.execute(
            """
            INSERT INTO titanic_booking (pclass, ticket, fare, cabin, embarked)
            SELECT pclass, ticket, fare, cabin, embarked FROM titanic_person
            """
        )
        op.execute(
            """
            UPDATE titanic_person AS p
            SET booking_id = b.id
            FROM titanic_booking AS b
            WHERE p.booking_id IS NULL
              AND p.pclass = b.pclass
              AND p.ticket = b.ticket
              AND p.fare = b.fare
              AND p.cabin = b.cabin
              AND p.embarked = b.embarked
            """
        )
        for col in ("pclass", "ticket", "fare", "cabin", "embarked"):
            op.drop_column("titanic_person", col)

    if "passenger_id" in booking_cols:
        try:
            op.drop_index("ix_titanic_booking_passenger_id", table_name="titanic_booking")
        except Exception:
            pass
        try:
            op.drop_constraint(
                "titanic_booking_passenger_id_key",
                "titanic_booking",
                type_="unique",
            )
        except Exception:
            pass
        try:
            op.drop_constraint(
                "titanic_booking_passenger_id_fkey",
                "titanic_booking",
                type_="foreignkey",
            )
        except Exception:
            pass
        op.drop_column("titanic_booking", "passenger_id")

    person_cols = {c["name"] for c in insp.get_columns("titanic_person")}
    if "booking_id" not in person_cols:
        op.add_column(
            "titanic_person",
            sa.Column("booking_id", sa.Integer(), nullable=True),
        )

    fks = {fk["name"] for fk in insp.get_foreign_keys("titanic_person")}
    if "fk_titanic_person_booking_id" not in fks:
        op.create_foreign_key(
            "fk_titanic_person_booking_id",
            "titanic_person",
            "titanic_booking",
            ["booking_id"],
            ["id"],
            ondelete="SET NULL",
        )
    uniques = {u["name"] for u in insp.get_unique_constraints("titanic_person")}
    if "uq_titanic_person_booking_id" not in uniques:
        op.create_unique_constraint(
            "uq_titanic_person_booking_id",
            "titanic_person",
            ["booking_id"],
        )


def downgrade() -> None:
    pass
