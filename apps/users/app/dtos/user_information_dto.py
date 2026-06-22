from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.database_manager import Base


class UserInformation(Base):
    """Neon `user_information` — 마이페이지 프로필 (회원 1명당 1행)."""

    __tablename__ = "user_information"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        name="id",
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("secom_users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    full_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(16), nullable=True)
    birth_date: Mapped[str | None] = mapped_column(String(8), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    favorite_exercise: Mapped[str | None] = mapped_column(String(32), nullable=True)
    favorite_exercise_other: Mapped[str | None] = mapped_column(String(128), nullable=True)
    exercise_experience: Mapped[str | None] = mapped_column(String(32), nullable=True)
    weekly_goal: Mapped[str | None] = mapped_column(String(32), nullable=True)
    health_note: Mapped[str | None] = mapped_column(Text, nullable=True)
