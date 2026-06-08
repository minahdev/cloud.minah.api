from sqlalchemy.ext.asyncio import AsyncSession

from inbody.dates import iso_utc, parse_date_key
from inbody.models.train_log_model import TrainDailyLog
from inbody.repositories.train_log_repository import TrainLogRepository
from inbody.schemas.train_log_schema import TrainDailyLogPayload, TrainDailyLogResponse
from inbody.user_lookup import require_user


def _to_response(row: TrainDailyLog) -> TrainDailyLogResponse:
    return TrainDailyLogResponse(
        date=row.log_date.isoformat(),
        muscles=list(row.muscles or []),
        workout=row.workout or "",
        weightKg=row.weight_kg,
        diet=dict(row.diet or {}),
        memo=row.memo or "",
        exerciseMinutes=row.exercise_minutes,
        updatedAt=iso_utc(row.updated_at),
    )


class TrainLogService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = TrainLogRepository(session)
        self._session = session

    async def list_logs(self, login_user_id: str) -> list[TrainDailyLogResponse]:
        user = await require_user(self._session, login_user_id)
        rows = await self._repo.list_for_user(user.id)
        return [_to_response(r) for r in rows]

    async def get(self, login_user_id: str, date_key: str) -> TrainDailyLogResponse | None:
        user = await require_user(self._session, login_user_id)
        row = await self._repo.get(user.id, parse_date_key(date_key))
        if row is None:
            return None
        return _to_response(row)

    async def save(self, payload: TrainDailyLogPayload) -> TrainDailyLogResponse:
        user = await require_user(self._session, payload.userId)
        row = await self._repo.upsert(
            user.id,
            parse_date_key(payload.date),
            payload.muscles,
            payload.workout,
            payload.weightKg,
            payload.diet,
            payload.memo,
            payload.exerciseMinutes,
        )
        return _to_response(row)
