from __future__ import annotations

from fastapi import APIRouter, Depends

from inbody.adapter.inbound.api.schemas.notice_schema import NoticeCreate, NoticeResponse
from inbody.app.dtos.notice_dto import NoticeCreateCommand, NoticeDeleteCommand, NoticeDto
from inbody.app.ports.input.notice_use_case import NoticeUseCase
from inbody.dependencies.notice_provider import get_notice_use_case

router = APIRouter(prefix="/inbody", tags=["inbody-notice"])


def _dto_to_resp(dto: NoticeDto) -> NoticeResponse:
    return NoticeResponse(
        id=dto.id,
        title=dto.title,
        body=dto.body,
        authorId=dto.author_id,
        createdAt=dto.created_at,
    )


@router.get("/notices", response_model=list[NoticeResponse])
async def list_notices(
    use_case: NoticeUseCase = Depends(get_notice_use_case),
):
    dtos = await use_case.list_notices()
    return [_dto_to_resp(d) for d in dtos]


@router.post("/notices", response_model=NoticeResponse)
async def create_notice(
    req: NoticeCreate,
    use_case: NoticeUseCase = Depends(get_notice_use_case),
) -> NoticeResponse:
    command = NoticeCreateCommand(user_id=req.userId, title=req.title, body=req.body)
    dto = await use_case.create_notice(command)
    return _dto_to_resp(dto)


@router.delete("/notices/{notice_id}")
async def delete_notice(
    notice_id: str,
    userId: str,
    use_case: NoticeUseCase = Depends(get_notice_use_case),
):
    command = NoticeDeleteCommand(user_id=userId, notice_id=notice_id)
    await use_case.delete_notice(command)
    return {"ok": True}
