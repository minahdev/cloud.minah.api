from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.adapter.outbound.orm.schedule_orm import Lesson
from inbody.app.dtos.schedule_dto import LessonDto
from inbody.app.ports.output.schedule_repository import ScheduleRepository


def _to_dto(row: Lesson) -> LessonDto:
    return LessonDto(
        id=str(row.id),
        date=row.lesson_date,
        title=row.title or "",
        time=row.time or "",
        schedule_note=row.schedule_note or "",
        created_at=row.created_at.isoformat() if row.created_at else "",
        member_user_id=str(row.member_user_id),
        record=row.record,
    )


class SchedulePgRepository(ScheduleRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_member(self, member_user_pk: int) -> list[LessonDto]:
        stmt = (
            select(Lesson)
            .where(Lesson.member_user_id == member_user_pk)
            .order_by(Lesson.lesson_date.desc(), Lesson.time)
        )
        result = await self._session.execute(stmt)
        return [_to_dto(r) for r in result.scalars().all()]

    async def upsert(
        self,
        member_user_pk: int,
        client_id: str,
        lesson_date: str,
        title: str,
        time: str,
        schedule_note: str,
        record: dict | None,
        created_at: datetime | None,
    ) -> LessonDto:
        stmt = select(Lesson).where(
            Lesson.member_user_id == member_user_pk,
            Lesson.client_id == client_id,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            row = Lesson(
                member_user_id=member_user_pk,
                client_id=client_id,
                lesson_date=lesson_date,
                title=title,
                time=time,
                schedule_note=schedule_note,
                record=record,
                created_at=created_at or datetime.now(timezone.utc),
            )
            self._session.add(row)
        else:
            row.lesson_date = lesson_date
            row.title = title
            row.time = time
            row.schedule_note = schedule_note
            row.record = record
        await self._session.commit()
        await self._session.refresh(row)
        return _to_dto(row)

    async def delete(self, member_user_pk: int, client_id: str) -> bool:
        stmt = select(Lesson).where(
            Lesson.member_user_id == member_user_pk,
            Lesson.client_id == client_id,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            return False
        await self._session.delete(row)
        await self._session.commit()
        return True
