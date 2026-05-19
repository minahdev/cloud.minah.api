from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    """Neon `secom_users` — 회원가입·로그인."""

    __tablename__ = "secom_users"

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(254), index=True)
    nickname: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(32), default="user")


UserModel = User
