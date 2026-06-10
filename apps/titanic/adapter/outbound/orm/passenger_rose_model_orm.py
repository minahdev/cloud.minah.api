from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.theone_base import Base
from titanic.app.dtos.crew_james_director_dto import BookingCommand


class RoseModelOrm(Base):

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("passengers.passenger_id", ondelete="CASCADE"),
        nullable=False,
    )
    pclass: Mapped[str] = mapped_column(String(8), default="")
    ticket: Mapped[str] = mapped_column(String(64), default="")
    fare: Mapped[str] = mapped_column(String(32), default="")
    cabin: Mapped[str] = mapped_column(String(64), default="")
    embarked: Mapped[str] = mapped_column(String(8), default="")

    @classmethod
    def from_command(cls, passenger_id: str, cmd: BookingCommand) -> "RoseModelOrm":
        return cls(
            passenger_id=passenger_id,
            pclass=cmd.pclass or "",
            ticket=cmd.ticket or "",
            fare=cmd.fare or "",
            cabin=cmd.cabin or "",
            embarked=cmd.embarked or "",
        )
