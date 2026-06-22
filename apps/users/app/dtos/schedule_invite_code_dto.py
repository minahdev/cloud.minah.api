from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.database_manager import Base


class ScheduleInviteCode(Base):
    """코치가 발급한 스케줄 입장 일회용 코드 (해시만 저장)."""

    __tablename__ = "schedule_invite_codes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        name="id",
    )
    code_digest: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_by_user_id: Mapped[str] = mapped_column(String(64), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    max_uses: Mapped[int] = mapped_column(Integer, default=1)
    use_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
