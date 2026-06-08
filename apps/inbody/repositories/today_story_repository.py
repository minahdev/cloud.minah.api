from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.models.today_story_model import TodayStory


class TodayStoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(self, user_id: int) -> list[TodayStory]:
        stmt = (
            select(TodayStory)
            .where(TodayStory.user_id == user_id)
            .order_by(TodayStory.story_date.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, user_id: int, story_date: date) -> TodayStory | None:
        stmt = select(TodayStory).where(
            TodayStory.user_id == user_id,
            TodayStory.story_date == story_date,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(
        self,
        user_id: int,
        story_date: date,
        mood: str | None,
        story: str,
    ) -> TodayStory:
        row = await self.get(user_id, story_date)
        now = datetime.now(timezone.utc)
        if row is None:
            row = TodayStory(
                user_id=user_id,
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
        return row
