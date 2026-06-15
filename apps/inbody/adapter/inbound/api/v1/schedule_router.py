from __future__ import annotations

from fastapi import APIRouter, Depends

from inbody.adapter.inbound.api.schemas.schedule_schema import LessonPayload, LessonResponse
from inbody.app.dtos.schedule_dto import LessonDeleteCommand, LessonDto, LessonListQuery, LessonSaveCommand
from inbody.app.ports.input.schedule_use_case import ScheduleUseCase
from inbody.dependencies.schedule_provider import get_schedule_use_case

router = APIRouter(prefix="/inbody", tags=["inbody-schedule"])


def _dto_to_resp(dto: LessonDto) -> LessonResponse:
    return LessonResponse(
        id=dto.id,
        date=dto.date,
        title=dto.title,
        time=dto.time,
        scheduleNote=dto.schedule_note,
        record=dto.record,
        createdAt=dto.created_at,
        memberUserId=dto.member_user_id,
    )


@router.get("/lessons", response_model=list[LessonResponse])
async def list_lessons(
    userId: str,
    memberUserId: str | None = None,
    use_case: ScheduleUseCase = Depends(get_schedule_use_case),
):
    query = LessonListQuery(user_id=userId, member_user_id=memberUserId)
    dtos = await use_case.list_lessons(query)
    return [_dto_to_resp(d) for d in dtos]


@router.put("/lessons", response_model=LessonResponse)
async def put_lesson(
    req: LessonPayload,
    use_case: ScheduleUseCase = Depends(get_schedule_use_case),
) -> LessonResponse:
    command = LessonSaveCommand(
        user_id=req.userId,
        client_id=req.id,
        date=req.date,
        title=req.title,
        time=req.time,
        schedule_note=req.scheduleNote,
        member_user_id=req.memberUserId,
        record=req.record,
        created_at=req.createdAt,
    )
    dto = await use_case.save_lesson(command)
    return _dto_to_resp(dto)


@router.delete("/lessons/{client_id}")
async def delete_lesson(
    client_id: str,
    userId: str,
    memberUserId: str | None = None,
    use_case: ScheduleUseCase = Depends(get_schedule_use_case),
):
    command = LessonDeleteCommand(
        user_id=userId,
        client_id=client_id,
        member_user_id=memberUserId,
    )
    await use_case.delete_lesson(command)
    return {"ok": True}
