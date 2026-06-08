from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.models.train_log_model import TrainDailyLog


class TrainLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(self, user_id: int) -> list[TrainDailyLog]:
        stmt = (
            select(TrainDailyLog)
            .where(TrainDailyLog.user_id == user_id)
            .order_by(TrainDailyLog.log_date.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, user_id: int, log_date: date) -> TrainDailyLog | None:
        stmt = select(TrainDailyLog).where(
            TrainDailyLog.user_id == user_id,
            TrainDailyLog.log_date == log_date,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(
        self,
        user_id: int,
        log_date: date,
        muscles: list,
        workout: str,
        weight_kg: float | None,
        diet: dict,
        memo: str,
        exercise_minutes: int | None,
    ) -> TrainDailyLog:
        row = await self.get(user_id, log_date)
        now = datetime.now(timezone.utc)
        if row is None:
            row = TrainDailyLog(
                user_id=user_id,
                log_date=log_date,
                muscles=muscles,
                workout=workout,
                weight_kg=weight_kg,
                diet=diet,
                memo=memo,
                exercise_minutes=exercise_minutes,
                updated_at=now,
            )
            self._session.add(row)
        else:
            row.muscles = muscles
            row.workout = workout
            row.weight_kg = weight_kg
            row.diet = diet
            row.memo = memo
            row.exercise_minutes = exercise_minutes
            row.updated_at = now
        await self._session.commit()
        await self._session.refresh(row)
        return row
