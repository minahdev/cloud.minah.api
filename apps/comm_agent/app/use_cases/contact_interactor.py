from __future__ import annotations

import logging

from comm_agent.adapter.inbound.api.schemas.contact_schema import (
    ContactIntroduceSchema,
    ContactRecordSchema,
)
from comm_agent.app.dtos.contact_dto import ContactCommand, ContactView
from comm_agent.app.dtos.email_send_dto import IntroduceResponse
from comm_agent.app.ports.input.contact_use_case import ManageContactsUseCase
from comm_agent.app.ports.output.contact_port import ContactRepositoryPort

logger = logging.getLogger(__name__)


class ManageContactsInteractor(ManageContactsUseCase):
    def __init__(self, repository: ContactRepositoryPort) -> None:
        self._repository = repository

    async def upload_contacts(self, records: list[ContactRecordSchema]) -> int:
        commands = [
            ContactCommand(nickname=r.nickname.strip(), email=r.email.strip())
            for r in records
        ]
        saved = await self._repository.save_contacts(commands)
        logger.info("[ManageContacts] 주소록 업로드 | received=%d saved=%d", len(commands), saved)
        return saved

    async def list_contacts(self) -> list[ContactView]:
        return await self._repository.list_contacts()

    async def search_contacts(self, keyword: str) -> list[ContactView]:
        return await self._repository.search_contacts(keyword)

    async def introduce_myself(self, schema: ContactIntroduceSchema) -> IntroduceResponse:
        logger.info(
            "[ManageContacts] introduce_myself 진입 | id=%s name=%s", schema.id, schema.name
        )
        return IntroduceResponse(
            id=schema.id,
            name=schema.name,
            answer=f"안녕하세요, 저는 '{schema.name}'입니다. CSV로 받은 닉네임·이메일을 보관하고 받는 사람을 찾아주는 주소록이에요.",
        )
