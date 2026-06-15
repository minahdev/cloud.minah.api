from __future__ import annotations

from fastapi import APIRouter, Depends

from inbody.adapter.inbound.api.schemas.today_story_schema import TodayStoryPayload, TodayStoryResponse
from inbody.app.dtos.today_story_dto import TodayStorySaveCommand, TodayStoryDto
from inbody.app.ports.input.today_story_use_case import TodayStoryUseCase
from inbody.dependencies.today_story_provider import get_today_story_use_case

router = APIRouter(prefix="/inbody", tags=["inbody-today-story"])


def _dto_to_resp(dto: TodayStoryDto) -> TodayStoryResponse:
    return TodayStoryResponse(
        date=dto.date,
        mood=dto.mood,
        story=dto.story,
        updatedAt=dto.updated_at,
    )


@router.get("/today-stories", response_model=list[TodayStoryResponse])
async def list_today_stories(
    userId: str,
    use_case: TodayStoryUseCase = Depends(get_today_story_use_case),
):
    dtos = await use_case.list_stories(userId)
    return [_dto_to_resp(d) for d in dtos]


@router.get("/today-story", response_model=TodayStoryResponse | None)
async def get_today_story(
    userId: str,
    date: str | None = None,
    use_case: TodayStoryUseCase = Depends(get_today_story_use_case),
):
    dto = await use_case.get(userId, date)
    return _dto_to_resp(dto) if dto else None


@router.put("/today-story", response_model=TodayStoryResponse)
async def put_today_story(
    req: TodayStoryPayload,
    use_case: TodayStoryUseCase = Depends(get_today_story_use_case),
) -> TodayStoryResponse:
    command = TodayStorySaveCommand(
        user_id=req.userId,
        date=req.date,
        mood=req.mood,
        story=req.story,
    )
    dto = await use_case.save(command)
    return _dto_to_resp(dto)
