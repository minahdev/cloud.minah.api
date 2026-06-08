from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.schemas.schedule_schema import LessonPayload, LessonResponse
from inbody.services.schedule_service import ScheduleService


class ScheduleController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = ScheduleService(session)

    async def list_lessons(
        self, user_id: str, member_user_id: str | None
    ) -> list[LessonResponse]:
        try:
            return await self._service.list_lessons(user_id, member_user_id)
        except ValueError as e:
            msg = str(e)
            status = 403 if "입장 코드" in msg else 403
            raise HTTPException(status_code=status, detail=msg) from e

    async def save_lesson(self, payload: LessonPayload) -> LessonResponse:
        try:
            return await self._service.save_lesson(payload)
        except ValueError as e:
            msg = str(e)
            if "입장 코드" in msg:
                raise HTTPException(status_code=403, detail=msg) from e
            status = 403 if "수정" in msg else 404
            raise HTTPException(status_code=status, detail=msg) from e

    async def delete_lesson(
        self, user_id: str, client_id: str, member_user_id: str | None
    ) -> None:
        try:
            await self._service.delete_lesson(user_id, member_user_id, client_id)
        except ValueError as e:
            msg = str(e)
            if "입장 코드" in msg:
                raise HTTPException(status_code=403, detail=msg) from e
            status = 403 if "수정" in msg else 404
            raise HTTPException(status_code=status, detail=msg) from e
