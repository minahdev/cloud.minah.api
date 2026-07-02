from __future__ import annotations

from abc import ABC, abstractmethod

from comm_agent.app.dtos.received_mail_dto import ReceivedMailCommand, ReceivedMailView


class ReceivedMailRepositoryPort(ABC):
    """수신 메일 저장·조회 게이트웨이."""

    @abstractmethod
    async def save_mail(self, command: ReceivedMailCommand, embedding: list[float]) -> int:
        pass

    @abstractmethod
    async def list_mails(self) -> list[ReceivedMailView]:
        pass
