from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.database_manager import Base


class Lesson(Base):
    __tablename__ = "lessons"
    __table_args__ = (
        UniqueConstraint("member_user_id", "client_id", name="uq_lessons_member_client"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, name="id")
    member_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("secom_users.id", ondelete="CASCADE"), index=True
    )
    client_id: Mapped[str] = mapped_column(String(64), index=True)
    lesson_date: Mapped[str] = mapped_column(String(10), index=True)
    title: Mapped[str] = mapped_column(String(200), default="")
    time: Mapped[str] = mapped_column(String(16), default="")
    schedule_note: Mapped[str] = mapped_column(Text, default="")
    record: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
