from __future__ import annotations

from titanic.adapter.outbound.orm.booking_orm import BookingModel
from titanic.app.dtos.crew_james_director_dto import BookingCommand


class BookingMapper:
    """BookingModel(DB) ↔ BookingCommand(DTO) 변환.

    Booking 전용 도메인 엔티티가 생기면 BookingCommand → BookingEntity 로 교체한다.
    """

    @staticmethod
    def to_dto(orm: BookingModel) -> BookingCommand:
        return BookingCommand(
            pclass=orm.pclass or "",
            ticket=orm.ticket or "",
            fare=orm.fare or "",
            cabin=orm.cabin or "",
            embarked=orm.embarked or "",
        )

    @staticmethod
    def to_orm(passenger_id: int, dto: BookingCommand) -> BookingModel:
        return BookingModel(
            passenger_id=passenger_id,
            pclass=dto.pclass or "",
            ticket=dto.ticket or "",
            fare=dto.fare or "",
            cabin=dto.cabin or "",
            embarked=dto.embarked or "",
        )
