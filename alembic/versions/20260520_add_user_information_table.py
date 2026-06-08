"""create user_information and move profile data from secom_users

Revision ID: 20260520_user_info
Revises: 20260519_mypage
Create Date: 2026-05-20

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260520_user_info"
down_revision: Union[str, Sequence[str], None] = "20260519_mypage"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_information",
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("full_name", sa.String(length=64), nullable=True),
        sa.Column("birth_date", sa.String(length=8), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("favorite_exercise", sa.String(length=32), nullable=True),
        sa.Column("favorite_exercise_other", sa.String(length=128), nullable=True),
        sa.Column("exercise_experience", sa.String(length=32), nullable=True),
        sa.Column("weekly_goal", sa.String(length=32), nullable=True),
        sa.Column("health_note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["secom_users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.execute(
        """
        INSERT INTO user_information (
            user_id, full_name, birth_date, phone, height_cm, weight_kg,
            favorite_exercise, favorite_exercise_other, exercise_experience,
            weekly_goal, health_note
        )
        SELECT
            user_id, full_name, birth_date, phone, height_cm, weight_kg,
            favorite_exercise, favorite_exercise_other, exercise_experience,
            weekly_goal, health_note
        FROM secom_users
        WHERE full_name IS NOT NULL
           OR birth_date IS NOT NULL
           OR phone IS NOT NULL
           OR height_cm IS NOT NULL
           OR weight_kg IS NOT NULL
           OR favorite_exercise IS NOT NULL
           OR favorite_exercise_other IS NOT NULL
           OR exercise_experience IS NOT NULL
           OR weekly_goal IS NOT NULL
           OR health_note IS NOT NULL
        """
    )

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


def downgrade() -> None:
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

    op.execute(
        """
        UPDATE secom_users u
        SET
            full_name = i.full_name,
            birth_date = i.birth_date,
            phone = i.phone,
            height_cm = i.height_cm,
            weight_kg = i.weight_kg,
            favorite_exercise = i.favorite_exercise,
            favorite_exercise_other = i.favorite_exercise_other,
            exercise_experience = i.exercise_experience,
            weekly_goal = i.weekly_goal,
            health_note = i.health_note
        FROM user_information i
        WHERE u.user_id = i.user_id
        """
    )

    op.drop_table("user_information")
