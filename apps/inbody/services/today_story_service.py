from sqlalchemy.ext.asyncio import AsyncSession

from inbody.dates import iso_utc, parse_date_key
from inbody.models.today_story_model import TodayStory
from inbody.repositories.today_story_repository import TodayStoryRepository
from inbody.schemas.today_story_schema import TodayStoryPayload, TodayStoryResponse
from inbody.user_lookup import require_user
from secom.app.dtos.user_model import User


def _to_response(row: TodayStory, login_user_id: str) -> TodayStoryResponse:
    return TodayStoryResponse(
        date=row.story_date.isoformat(),
        mood=row.mood,
        story=row.story,
        updatedAt=iso_utc(row.updated_at),
    )


class TodayStoryService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = TodayStoryRepository(session)
        self._session = session

    async def list_stories(self, login_user_id: str) -> list[TodayStoryResponse]:
        user = await require_user(self._session, login_user_id)
        rows = await self._repo.list_for_user(user.id)
        return [_to_response(r, user.user_id) for r in rows]

    async def get(self, login_user_id: str, date_key: str | None) -> TodayStoryResponse | None:
        user = await require_user(self._session, login_user_id)
        row = await self._repo.get(user.id, parse_date_key(date_key))
        if row is None:
            return None
        return _to_response(row, user.user_id)

    async def save(self, payload: TodayStoryPayload) -> TodayStoryResponse:
        user = await require_user(self._session, payload.userId)
        story_date = parse_date_key(payload.date)
        row = await self._repo.upsert(
            user.id,
            story_date,
            payload.mood,
            payload.story.strip(),
        )
        return _to_response(row, user.user_id)
