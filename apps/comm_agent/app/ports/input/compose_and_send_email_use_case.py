from __future__ import annotations

from abc import ABC, abstractmethod

from comm_agent.app.dtos.send_email_dto import SendEmailCommand, SendEmailResponse


class ComposeAndSendEmailUseCase(ABC):
    """주제로 본문을 생성해 이메일을 발송한다."""

    @abstractmethod
    async def compose_and_send(self, command: SendEmailCommand) -> SendEmailResponse:
        pass
