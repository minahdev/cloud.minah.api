from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.models.schedule_model import Lesson


class ScheduleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_member(self, member_user_id: int) -> list[Lesson]:
        stmt = (
            select(Lesson)
            .where(Lesson.member_user_id == member_user_id)
            .order_by(Lesson.lesson_date.desc(), Lesson.time)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_client_id(
        self, member_user_id: int, client_id: str
    ) -> Lesson | None:
        stmt = select(Lesson).where(
            Lesson.member_user_id == member_user_id,
            Lesson.client_id == client_id,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(
        self,
        member_user_id: int,
        client_id: str,
        lesson_date: str,
        title: str,
        time: str,
        schedule_note: str,
        record: dict | None,
        created_at: datetime | None,
    ) -> Lesson:
        row = await self.get_by_client_id(member_user_id, client_id)
        if row is None:
            row = Lesson(
                member_user_id=member_user_id,
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
        return row

    async def delete(self, member_user_id: int, client_id: str) -> bool:
        row = await self.get_by_client_id(member_user_id, client_id)
        if row is None:
            return False
        await self._session.delete(row)
        await self._session.commit()
        return True
