"""add mypage profile columns to secom_users

Revision ID: 20260519_mypage
Revises:
Create Date: 2026-05-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260519_mypage"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("secom_users", sa.Column("full_name", sa.String(length=64), nullable=True))
    op.add_column("secom_users", sa.Column("birth_date", sa.String(length=8), nullable=True))
    op.add_column("secom_users", sa.Column("phone", sa.String(length=32), nullable=True))
    op.add_column("secom_users", sa.Column("height_cm", sa.Float(), nullable=True))
    op.add_column("secom_users", sa.Column("weight_kg", sa.Float(), nullable=True))
    op.add_column("secom_users", sa.Column("favorite_exercise", sa.String(length=32), nullable=True))
    op.add_column(
        "secom_users", sa.Column("favorite_exercise_other", sa.String(length=128), nullable=True)
    )
    op.add_column("secom_users", sa.Column("exercise_experience", sa.String(length=32), nullable=True))
    op.add_column("secom_users", sa.Column("weekly_goal", sa.String(length=32), nullable=True))
    op.add_column("secom_users", sa.Column("health_note", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("secom_users", "health_note")
    op.drop_column("secom_users", "weekly_goal")
    op.drop_column("secom_users", "exercise_experience")
    op.drop_column("secom_users", "favorite_exercise_other")
    op.drop_column("secom_users", "favorite_exercise")
    op.drop_column("secom_users", "weight_kg")
    op.drop_column("secom_users", "height_cm")
    op.drop_column("secom_users", "phone")
    op.drop_column("secom_users", "birth_date")
    op.drop_column("secom_users", "full_name")
