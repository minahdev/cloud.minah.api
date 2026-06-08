from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.schemas.train_log_schema import TrainDailyLogPayload, TrainDailyLogResponse
from inbody.services.train_log_service import TrainLogService


class TrainLogController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = TrainLogService(session)

    async def list_logs(self, user_id: str) -> list[TrainDailyLogResponse]:
        try:
            return await self._service.list_logs(user_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    async def get(self, user_id: str, date_key: str) -> TrainDailyLogResponse | None:
        try:
            return await self._service.get(user_id, date_key)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    async def save(self, payload: TrainDailyLogPayload) -> TrainDailyLogResponse:
        try:
            return await self._service.save(payload)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
