from __future__ import annotations

from fastapi import APIRouter, Depends

from inbody.adapter.inbound.api.schemas.train_log_schema import TrainDailyLogPayload, TrainDailyLogResponse
from inbody.app.dtos.train_log_dto import TrainLogDto, TrainLogSaveCommand
from inbody.app.ports.input.train_log_use_case import TrainLogUseCase
from inbody.dependencies.train_log_provider import get_train_log_use_case

router = APIRouter(prefix="/inbody", tags=["inbody-train-log"])


def _dto_to_resp(dto: TrainLogDto) -> TrainDailyLogResponse:
    return TrainDailyLogResponse(
        date=dto.date,
        muscles=dto.muscles,
        workout=dto.workout,
        weightKg=dto.weight_kg,
        diet=dto.diet,
        memo=dto.memo,
        exerciseMinutes=dto.exercise_minutes,
        updatedAt=dto.updated_at,
    )


@router.get("/train-logs", response_model=list[TrainDailyLogResponse])
async def list_train_logs(
    userId: str,
    use_case: TrainLogUseCase = Depends(get_train_log_use_case),
):
    dtos = await use_case.list_logs(userId)
    return [_dto_to_resp(d) for d in dtos]


@router.get("/train-logs/day", response_model=TrainDailyLogResponse | None)
async def get_train_log_day(
    userId: str,
    date: str,
    use_case: TrainLogUseCase = Depends(get_train_log_use_case),
):
    dto = await use_case.get(userId, date)
    return _dto_to_resp(dto) if dto else None


@router.put("/train-logs", response_model=TrainDailyLogResponse)
async def put_train_log(
    req: TrainDailyLogPayload,
    use_case: TrainLogUseCase = Depends(get_train_log_use_case),
) -> TrainDailyLogResponse:
    command = TrainLogSaveCommand(
        user_id=req.userId,
        date=req.date,
        muscles=req.muscles,
        workout=req.workout,
        weight_kg=req.weightKg,
        diet=req.diet,
        memo=req.memo,
        exercise_minutes=req.exerciseMinutes,
    )
    dto = await use_case.save(command)
    return _dto_to_resp(dto)
