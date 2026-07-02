from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from comm_agent.app.dtos.received_mail_dto import (
    ReceivedMailCommand,
    ReceivedMailResponse,
    ReceivedMailView,
)

if TYPE_CHECKING:
    from comm_agent.adapter.inbound.api.schemas.receive_mail_schema import (
        ReceivedMailIntroduceSchema,
    )


class ReceiveMailUseCase(ABC):
    """수신 메일 저장·목록 조회."""

    @abstractmethod
    async def save_incoming(self, command: ReceivedMailCommand) -> int:
        pass

    @abstractmethod
    async def list_received(self) -> list[ReceivedMailView]:
        pass

    @abstractmethod
    async def introduce_myself(self, schema: ReceivedMailIntroduceSchema) -> ReceivedMailResponse:
        pass
