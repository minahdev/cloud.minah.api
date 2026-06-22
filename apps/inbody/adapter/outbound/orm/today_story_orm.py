from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.database_manager import Base


class TodayStory(Base):
    __tablename__ = "today_stories"
    __table_args__ = (UniqueConstraint("user_id", "story_date", name="uq_today_stories_user_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, name="id")
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("secom_users.id", ondelete="CASCADE"), index=True
    )
    story_date: Mapped[date] = mapped_column(Date, index=True)
    mood: Mapped[str | None] = mapped_column(String(16), nullable=True)
    story: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
