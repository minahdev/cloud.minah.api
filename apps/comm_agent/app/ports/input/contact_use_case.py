from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from comm_agent.app.dtos.contact_dto import ContactView
from comm_agent.app.dtos.email_send_dto import IntroduceResponse

if TYPE_CHECKING:
    from comm_agent.adapter.inbound.api.schemas.contact_schema import (
        ContactIntroduceSchema,
        ContactRecordSchema,
    )


class ManageContactsUseCase(ABC):
    """주소록 업로드(CSV)·목록 조회."""

    @abstractmethod
    async def upload_contacts(self, records: list[ContactRecordSchema]) -> int:
        pass

    @abstractmethod
    async def list_contacts(self) -> list[ContactView]:
        pass

    @abstractmethod
    async def search_contacts(self, keyword: str) -> list[ContactView]:
        pass

    @abstractmethod
    async def introduce_myself(self, schema: ContactIntroduceSchema) -> IntroduceResponse:
        pass
