from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from titanic.app.dtos.crew_james_director_dto import BookingCommand
from titanic.adapter.outbound.orm.passenger_orm import parse_passenger_id


class BookingModel(Base):
    """`BookingCommand` + `passenger_id`(integer PK/FK)."""

    __tablename__ = "titanic_booking"

    passenger_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("titanic_person.passenger_id", ondelete="CASCADE"),
        primary_key=True,
    )
    pclass: Mapped[str] = mapped_column(String(8), default="")
    ticket: Mapped[str] = mapped_column(String(64), default="")
    fare: Mapped[str] = mapped_column(String(32), default="")
    cabin: Mapped[str] = mapped_column(String(64), default="")
    embarked: Mapped[str] = mapped_column(String(8), default="")

    @classmethod
    def from_command(cls, passenger_id: str, cmd: BookingCommand) -> BookingModel | None:
        pid = parse_passenger_id(passenger_id)
        if pid is None:
            return None
        return cls(
            passenger_id=pid,
            pclass=cmd.pclass or "",
            ticket=cmd.ticket or "",
            fare=cmd.fare or "",
            cabin=cmd.cabin or "",
            embarked=cmd.embarked or "",
        )
