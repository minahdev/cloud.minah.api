from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.theone_base import Base

class JackTrainerOrm(Base):
    __tablename__ = "passengers"

    passenger_id: Mapped[str | None] = mapped_column(String, primary_key=True, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[str | None] = mapped_column(String, nullable=True)
    sib_sp: Mapped[str | None] = mapped_column(String, nullable=True)
    parch: Mapped[str | None] = mapped_column(String, nullable=True)
    survived: Mapped[str | None] = mapped_column(String, nullable=True)

def parse_passenger_id(value: str | None) -> int | None:
    """문자열 passenger_id → 정수 변환. 파싱 실패 시 None 반환."""
    if not value:
        return None
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return None


# 하위 호환 alias
TitanicRecord = JackTrainerOrm
PassengerModel = JackTrainerOrm
