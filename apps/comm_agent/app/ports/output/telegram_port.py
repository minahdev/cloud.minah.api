from __future__ import annotations

from abc import ABC, abstractmethod

from comm_agent.app.dtos.telegram_dto import TelegramResponse, TelegramSendQuery


class TelegramSenderPort(ABC):
    """텔레그램 발송 게이트웨이 (구현체는 Telegram Bot API)."""

    @abstractmethod
    async def send(self, chat_id: str, text: str) -> dict:
        pass

    @abstractmethod
    def introduce_myself(self, query: TelegramSendQuery)-> TelegramResponse:
        pass
