"""foods table

Revision ID: 20260615_01
Revises: 20260604_07
Create Date: 2026-06-15

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260615_01"
down_revision: Union[str, None] = "20260604_07"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "foods",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("calories_kcal", sa.Float(), nullable=False),
        sa.Column("protein_g", sa.Float(), nullable=False, server_default="0"),
        sa.Column("carbs_g", sa.Float(), nullable=False, server_default="0"),
        sa.Column("fat_g", sa.Float(), nullable=False, server_default="0"),
        sa.Column("serving_size", sa.Float(), nullable=False, server_default="1"),
        sa.Column("serving_unit", sa.String(length=20), nullable=False, server_default="인분"),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_foods_name", "foods", ["name"])


def downgrade() -> None:
    op.drop_index("ix_foods_name", table_name="foods")
    op.drop_table("foods")
