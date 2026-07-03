from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from comm_agent.app.dtos.telegram_dto import (
    TelegramResponse,
    TelegramSendCommand,
    TelegramSendResponse,
)

if TYPE_CHECKING:
    from comm_agent.adapter.inbound.api.schemas.telegram_schema import (
        TelegramIntroduceSchema,
    )


class TelegramUseCase(ABC):
    """Telegram 채널 유스케이스."""

    @abstractmethod
    async def send_message(self, command: TelegramSendCommand) -> TelegramSendResponse:
        pass

    @abstractmethod
    async def send_report(self, chat_id: str, text: str) -> bool:
        """가공 없이 raw 텍스트를 발송 (업무보고용). 실패해도 예외 대신 False."""
        pass

    @abstractmethod
    async def introduce_myself(self, schema: TelegramIntroduceSchema) -> TelegramResponse:
        pass
