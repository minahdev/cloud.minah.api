from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.database_manager import Base


class User(Base):
    """Neon `secom_users` — 회원가입·로그인."""

    __tablename__ = "secom_users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        name="id",
    )
    user_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(254), index=True)
    nickname: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(32), default="user")


UserModel = User
