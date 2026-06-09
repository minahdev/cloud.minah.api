from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from titanic.app.dtos.crew_james_director_dto import PassengerCommand


def parse_passenger_id(raw: str) -> int | None:
    text = (raw or "").strip()
    if not text.isdigit():
        return None
    return int(text)


class PassengerModel(Base):
    """James `PassengerCommand` → `titanic_passenger` (`passenger_id`는 DB에서 integer)."""

    __tablename__ = "titanic_passenger"

    passenger_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    gender: Mapped[str] = mapped_column(String(16), default="")
    age: Mapped[str] = mapped_column(String(16), default="")
    sib_sp: Mapped[str] = mapped_column(String(16), default="")
    parch: Mapped[str] = mapped_column(String(16), default="")
    survived: Mapped[str] = mapped_column(String(8), default="")

    @classmethod
    def from_command(cls, cmd: PassengerCommand) -> PassengerModel | None:
        pid = parse_passenger_id(cmd.passenger_id)
        if pid is None:
            return None
        return cls(
            passenger_id=pid,
            name=cmd.name or "",
            gender=cmd.gender or "",
            age=cmd.age or "",
            sib_sp=cmd.sib_sp or "",
            parch=cmd.parch or "",
            survived=cmd.survived or "",
        )
