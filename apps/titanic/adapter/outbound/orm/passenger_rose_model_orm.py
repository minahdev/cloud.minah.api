from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.theone_base import Base


class RoseModelOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[str | None] = mapped_column(String, nullable=True)
    pclass: Mapped[str | None] = mapped_column(String, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String, nullable=True)
    fare: Mapped[str | None] = mapped_column(String, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String, nullable=True)
    embarked: Mapped[str | None] = mapped_column(String, nullable=True)
