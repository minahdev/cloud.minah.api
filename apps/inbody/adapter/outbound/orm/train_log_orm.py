from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.database_manager import Base


class TrainDailyLog(Base):
    __tablename__ = "train_daily_logs"
    __table_args__ = (UniqueConstraint("user_id", "log_date", name="uq_train_daily_logs_user_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, name="id")
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("secom_users.id", ondelete="CASCADE"), index=True
    )
    log_date: Mapped[date] = mapped_column(Date, index=True)
    muscles: Mapped[list] = mapped_column(JSONB, default=list)
    workout: Mapped[str] = mapped_column(Text, default="")
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    diet: Mapped[dict] = mapped_column(JSONB, default=dict)
    memo: Mapped[str] = mapped_column(Text, default="")
    exercise_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
