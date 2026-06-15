from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.adapter.outbound.orm.train_log_orm import TrainDailyLog
from inbody.app.dtos.train_log_dto import TrainLogDto
from inbody.app.ports.output.train_log_repository import TrainLogRepository


def _to_dto(row: TrainDailyLog) -> TrainLogDto:
    return TrainLogDto(
        date=str(row.log_date),
        updated_at=row.updated_at.isoformat() if row.updated_at else "",
        muscles=list(row.muscles or []),
        workout=row.workout or "",
        weight_kg=row.weight_kg,
        diet=dict(row.diet or {}),
        memo=row.memo or "",
        exercise_minutes=row.exercise_minutes,
    )


class TrainLogPgRepository(TrainLogRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(self, user_pk: int) -> list[TrainLogDto]:
        stmt = (
            select(TrainDailyLog)
            .where(TrainDailyLog.user_id == user_pk)
            .order_by(TrainDailyLog.log_date.desc())
        )
        result = await self._session.execute(stmt)
        return [_to_dto(r) for r in result.scalars().all()]

    async def get(self, user_pk: int, log_date: date) -> TrainLogDto | None:
        stmt = select(TrainDailyLog).where(
            TrainDailyLog.user_id == user_pk,
            TrainDailyLog.log_date == log_date,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return _to_dto(row) if row else None

    async def upsert(
        self,
        user_pk: int,
        log_date: date,
        muscles: list,
        workout: str,
        weight_kg: float | None,
        diet: dict,
        memo: str,
        exercise_minutes: int | None,
    ) -> TrainLogDto:
        stmt = select(TrainDailyLog).where(
            TrainDailyLog.user_id == user_pk,
            TrainDailyLog.log_date == log_date,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        now = datetime.now(timezone.utc)
        if row is None:
            row = TrainDailyLog(
                user_id=user_pk,
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
        return _to_dto(row)
