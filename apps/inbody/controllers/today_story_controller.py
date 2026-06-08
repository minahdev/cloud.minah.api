from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.schemas.today_story_schema import TodayStoryPayload, TodayStoryResponse
from inbody.services.today_story_service import TodayStoryService


class TodayStoryController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = TodayStoryService(session)

    async def list_stories(self, user_id: str) -> list[TodayStoryResponse]:
        return await self._service.list_stories(user_id)

    async def get(self, user_id: str, date_key: str | None) -> TodayStoryResponse | None:
        return await self._service.get(user_id, date_key)

    async def save(self, payload: TodayStoryPayload) -> TodayStoryResponse:
        try:
            return await self._service.save(payload)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
