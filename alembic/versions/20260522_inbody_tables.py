"""inbody content tables

Revision ID: 20260522_inbody
Revises: 20260521_entity_id_pk
Create Date: 2026-05-22

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260522_inbody"
down_revision: Union[str, None] = "20260521_entity_id"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "today_stories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("story_date", sa.Date(), nullable=False),
        sa.Column("mood", sa.String(length=16), nullable=True),
        sa.Column("story", sa.Text(), nullable=False, server_default=""),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["secom_users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "story_date", name="uq_today_stories_user_date"),
    )
    op.create_index("ix_today_stories_user_id", "today_stories", ["user_id"])
    op.create_index("ix_today_stories_story_date", "today_stories", ["story_date"])

    op.create_table(
        "train_daily_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("log_date", sa.Date(), nullable=False),
        sa.Column("muscles", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("workout", sa.Text(), nullable=False, server_default=""),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("diet", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("memo", sa.Text(), nullable=False, server_default=""),
        sa.Column("exercise_minutes", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["secom_users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "log_date", name="uq_train_daily_logs_user_date"),
    )
    op.create_index("ix_train_daily_logs_user_id", "train_daily_logs", ["user_id"])
    op.create_index("ix_train_daily_logs_log_date", "train_daily_logs", ["log_date"])

    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("member_user_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.String(length=64), nullable=False),
        sa.Column("lesson_date", sa.String(length=10), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("time", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("schedule_note", sa.Text(), nullable=False, server_default=""),
        sa.Column("record", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["member_user_id"], ["secom_users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("member_user_id", "client_id", name="uq_lessons_member_client"),
    )
    op.create_index("ix_lessons_member_user_id", "lessons", ["member_user_id"])
    op.create_index("ix_lessons_client_id", "lessons", ["client_id"])
    op.create_index("ix_lessons_lesson_date", "lessons", ["lesson_date"])

    op.create_table(
        "community_posts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("author_user_id", sa.Integer(), nullable=False),
        sa.Column("workout_type", sa.String(length=64), nullable=False, server_default="기타"),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["author_user_id"], ["secom_users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_community_posts_author_user_id", "community_posts", ["author_user_id"])
    op.create_index("ix_community_posts_created_at", "community_posts", ["created_at"])

    op.create_table(
        "notices",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("author_user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["author_user_id"], ["secom_users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_notices_author_user_id", "notices", ["author_user_id"])
    op.create_index("ix_notices_created_at", "notices", ["created_at"])


def downgrade() -> None:
    op.drop_table("notices")
    op.drop_table("community_posts")
    op.drop_table("lessons")
    op.drop_table("train_daily_logs")
    op.drop_table("today_stories")
