from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.theone_base import Base


class BookingModel(Base):
    __tablename__ = "titanic_booking"

    passenger_id: Mapped[int] = mapped_column(Integer, ForeignKey("titanic_person.passenger_id"), primary_key=True)
    pclass: Mapped[str | None] = mapped_column(String, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String, nullable=True)
    fare: Mapped[str | None] = mapped_column(String, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String, nullable=True)
    embarked: Mapped[str | None] = mapped_column(String, nullable=True)
