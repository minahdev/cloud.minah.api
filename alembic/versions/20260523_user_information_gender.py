"""add gender to user_information

Revision ID: 20260523_gender
Revises: 20260522_inbody
Create Date: 2026-05-23

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260523_gender"
down_revision: Union[str, None] = "20260522_inbody"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_information",
        sa.Column("gender", sa.String(length=16), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("user_information", "gender")
