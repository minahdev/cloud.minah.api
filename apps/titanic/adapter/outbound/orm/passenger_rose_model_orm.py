from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from minahai.core.matrix.theone_base import Base

class RoseModelOrm(Base):

    __tablename__ = "bookings"

    passenger_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    gender: Mapped[str] = mapped_column(String(16), default="")
    age: Mapped[str] = mapped_column(String(16), default="")
    sib_sp: Mapped[str] = mapped_column(String(16), default="")
    parch: Mapped[str] = mapped_column(String(16), default="")
    survived: Mapped[str] = mapped_column(String(8), default="")