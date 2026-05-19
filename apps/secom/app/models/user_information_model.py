from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserInformation(Base):
    """Neon `user_information` — 마이페이지 프로필 (회원 1명당 1행)."""

    __tablename__ = "user_information"

    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("secom_users.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    full_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    birth_date: Mapped[str | None] = mapped_column(String(8), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    favorite_exercise: Mapped[str | None] = mapped_column(String(32), nullable=True)
    favorite_exercise_other: Mapped[str | None] = mapped_column(String(128), nullable=True)
    exercise_experience: Mapped[str | None] = mapped_column(String(32), nullable=True)
    weekly_goal: Mapped[str | None] = mapped_column(String(32), nullable=True)
    health_note: Mapped[str | None] = mapped_column(Text, nullable=True)
