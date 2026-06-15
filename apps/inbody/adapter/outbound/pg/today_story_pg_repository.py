from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.adapter.outbound.orm.today_story_orm import TodayStory
from inbody.app.dtos.today_story_dto import TodayStoryDto
from inbody.app.ports.output.today_story_repository import TodayStoryRepository


def _to_dto(row: TodayStory) -> TodayStoryDto:
    return TodayStoryDto(
        date=str(row.story_date),
        mood=row.mood,
        story=row.story,
        updated_at=row.updated_at.isoformat() if row.updated_at else "",
    )


class TodayStoryPgRepository(TodayStoryRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(self, user_pk: int) -> list[TodayStoryDto]:
        stmt = (
            select(TodayStory)
            .where(TodayStory.user_id == user_pk)
            .order_by(TodayStory.story_date.desc())
        )
        result = await self._session.execute(stmt)
        return [_to_dto(r) for r in result.scalars().all()]

    async def get(self, user_pk: int, story_date: date) -> TodayStoryDto | None:
        stmt = select(TodayStory).where(
            TodayStory.user_id == user_pk,
            TodayStory.story_date == story_date,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return _to_dto(row) if row else None

    async def upsert(
        self,
        user_pk: int,
        story_date: date,
        mood: str | None,
        story: str,
    ) -> TodayStoryDto:
        stmt = select(TodayStory).where(
            TodayStory.user_id == user_pk,
            TodayStory.story_date == story_date,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        now = datetime.now(timezone.utc)
        if row is None:
            row = TodayStory(
                user_id=user_pk,
                story_date=story_date,
                mood=mood,
                story=story,
                updated_at=now,
            )
            self._session.add(row)
        else:
            row.mood = mood
            row.story = story
            row.updated_at = now
        await self._session.commit()
        await self._session.refresh(row)
        return _to_dto(row)
