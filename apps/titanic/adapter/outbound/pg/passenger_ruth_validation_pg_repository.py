from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
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


class RuthValidationPgRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_by_pclass(
        self, pclass: int, page: int, page_size: int
    ) -> tuple[int, list[dict[str, Any]]]:
        """등급(pclass)으로 필터링한 승객 목록 페이지네이션 조회"""
        pclass_str = str(pclass)
        total = (
            await self.session.execute(
                select(func.count())
                .select_from(PersonOrm)
                .join(BookingOrm, BookingOrm.person_id == PersonOrm.id)
                .where(BookingOrm.pclass == pclass_str)
            )
        ).scalar_one()
        rows = (
            await self.session.execute(
                select(PersonOrm, BookingOrm)
                .join(BookingOrm, BookingOrm.person_id == PersonOrm.id)
                .where(BookingOrm.pclass == pclass_str)
                .order_by(PersonOrm.id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
        ).all()
        items = [_row_to_dict(person, booking) for person, booking in rows]
        return total, items