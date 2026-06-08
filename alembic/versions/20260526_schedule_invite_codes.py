"""schedule_invite_codes for coach-issued one-time schedule access

Revision ID: 20260526_invite_codes
Revises: 20260523_gender
Create Date: 2026-05-26

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260526_invite_codes"
down_revision: Union[str, None] = "20260523_gender"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "schedule_invite_codes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code_digest", sa.String(length=64), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("max_uses", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("use_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code_digest", name="uq_schedule_invite_codes_code_digest"),
    )
    op.create_index(
        "ix_schedule_invite_codes_created_by_user_id",
        "schedule_invite_codes",
        ["created_by_user_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_schedule_invite_codes_created_by_user_id", table_name="schedule_invite_codes")
    op.drop_table("schedule_invite_codes")
