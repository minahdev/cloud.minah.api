from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.database_manager import Base


class ScheduleAccessGrant(Base):
    """스케줄 접근 암호를 맞게 입력한 회원 (코치 탭·입장 허용 목록)."""

    __tablename__ = "schedule_access_grants"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        name="id",
    )
    user_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
