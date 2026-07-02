from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from comm_agent.app.dtos.email_send_dto import (
    IntroduceResponse,
    SendEmailCommand,
    SendEmailResponse,
)

if TYPE_CHECKING:
    from comm_agent.adapter.inbound.api.schemas.send_email_schema import (
        ComposeEmailIntroduceSchema,
    )


class ComposeAndSendEmailUseCase(ABC):
    """주제로 본문을 생성해 이메일을 발송한다."""

    @abstractmethod
    async def compose_and_send(self, command: SendEmailCommand) -> SendEmailResponse:
        pass

    @abstractmethod
    async def introduce_myself(self, schema: ComposeEmailIntroduceSchema) -> IntroduceResponse:
        pass
