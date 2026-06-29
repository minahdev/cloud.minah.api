from __future__ import annotations

from abc import ABC, abstractmethod


class EmailSenderPort(ABC):
    """이메일 발송 게이트웨이 (구현체는 n8n·SMTP 등 외부 시스템)."""

    @abstractmethod
    async def send(self, to: str, subject: str, body: str) -> dict:
        pass
