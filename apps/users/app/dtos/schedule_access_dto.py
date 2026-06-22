from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.database_manager import Base


class ScheduleAccess(Base):
    """레슨 스케줄 접근 암호 (앱 전체 1건). 코치가 설정, 회원이 입력 후 이용."""

    __tablename__ = "schedule_access"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        name="id",
    )
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    updated_by_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
