from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.schemas.notice_schema import NoticeCreate, NoticeResponse
from inbody.services.notice_service import NoticeService


class NoticeController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = NoticeService(session)

    async def list_notices(self) -> list[NoticeResponse]:
        return await self._service.list_notices()

    async def create_notice(self, payload: NoticeCreate) -> NoticeResponse:
        try:
            return await self._service.create_notice(payload)
        except ValueError as e:
            raise HTTPException(status_code=403, detail=str(e)) from e

    async def delete_notice(self, user_id: str, notice_id: str) -> None:
        try:
            await self._service.delete_notice(user_id, notice_id)
        except ValueError as e:
            raise HTTPException(status_code=403, detail=str(e)) from e
