from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from comm_agent.adapter.inbound.api.contact_csv_parser import (
    ContactCsvParseError,
    parse_contacts_csv_text,
)
from comm_agent.adapter.inbound.api.schemas.contact_schema import (
    ContactIntroduceSchema,
    ContactViewSchema,
    UploadContactsResponseSchema,
)
from comm_agent.app.dtos.email_send_dto import IntroduceResponse
from comm_agent.app.ports.input.contact_use_case import ManageContactsUseCase
from comm_agent.dependencies.contact_provider import get_manage_contacts_use_case

logger = logging.getLogger(__name__)

contact_router = APIRouter(prefix="/comm_agent/contacts", tags=["comm_agent_contacts"])


@contact_router.post("/upload", response_model=UploadContactsResponseSchema)
async def upload_contacts(
    file: UploadFile = File(...),
    use_case: ManageContactsUseCase = Depends(get_manage_contacts_use_case),
) -> UploadContactsResponseSchema:
    """CSV(닉네임,이메일)를 업로드해 주소록에 저장한다. (titanic 업로드와 동일 패턴)"""
    raw = await file.read()
    text = raw.decode("utf-8-sig", errors="replace")
    try:
        records = parse_contacts_csv_text(text)
    except ContactCsvParseError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    saved = await use_case.upload_contacts(records)
    return UploadContactsResponseSchema(saved=saved)


@contact_router.get("", response_model=list[ContactViewSchema])
async def list_contacts(
    use_case: ManageContactsUseCase = Depends(get_manage_contacts_use_case),
) -> list[ContactViewSchema]:
    """주소록 목록을 돌려준다."""
    views = await use_case.list_contacts()
    return [ContactViewSchema(id=v.id, nickname=v.nickname, email=v.email) for v in views]


@contact_router.get("/search", response_model=list[ContactViewSchema])
async def search_contacts(
    q: str = "",
    use_case: ManageContactsUseCase = Depends(get_manage_contacts_use_case),
) -> list[ContactViewSchema]:
    """이름/성/이메일로 주소록을 검색한다."""
    views = await use_case.search_contacts(q)
    return [ContactViewSchema(id=v.id, nickname=v.nickname, email=v.email) for v in views]


@contact_router.get("/myself", response_model=IntroduceResponse)
async def introduce_myself(
    use_case: ManageContactsUseCase = Depends(get_manage_contacts_use_case),
) -> IntroduceResponse:
    """주소록 자기소개."""
    return await use_case.introduce_myself(
        ContactIntroduceSchema(
            id=1,
            name="Address Book",
        )
    )


