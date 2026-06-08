from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.passenger_orm import PersonOrm


def _row_to_dict(person: PersonOrm, booking: BookingOrm | None) -> dict[str, Any]:
    return {
        "id": person.id,
        "passenger": person.passenger_id,
        "survived": person.survived,
        "pclass": booking.pclass if booking else None,
        "name": person.name,
        "gender": person.gender,
        "age": person.age,
        "sibsp": person.sib_sp,
        "parch": person.parch,
        "ticket": booking.ticket if booking else None,
        "fare": booking.fare if booking else None,
        "cabin": booking.cabin if booking else None,
        "embarked": booking.embarked if booking else None,
    }


class RoseModelPgRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_records(self) -> list[dict[str, Any]]:
        """ML 학습에 사용할 전체 승객 데이터 조회"""
        rows = (
            await self.session.execute(
                select(PersonOrm, BookingOrm)
                .outerjoin(BookingOrm, BookingOrm.person_id == PersonOrm.id)
                .order_by(PersonOrm.id)
            )
        ).all()
        return [_row_to_dict(person, booking) for person, booking in rows]