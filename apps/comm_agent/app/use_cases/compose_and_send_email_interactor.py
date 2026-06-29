from __future__ import annotations

import logging

from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator

from comm_agent.app.dtos.send_email_dto import SendEmailCommand, SendEmailResponse
from comm_agent.app.ports.input.compose_and_send_email_use_case import ComposeAndSendEmailUseCase
from comm_agent.app.ports.output.email_sender_port import EmailSenderPort

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "너는 이메일 본문을 작성하는 비서다. "
    "주어진 주제로 한국어 이메일 본문을 작성해라. "
    "인사말과 맺음말을 포함하고, 제목이나 머리말 없이 본문만 출력해라."
)


class ComposeAndSendEmailInteractor(ComposeAndSendEmailUseCase):
    def __init__(self, email_sender: EmailSenderPort) -> None:
        self._email_sender = email_sender

    async def compose_and_send(self, command: SendEmailCommand) -> SendEmailResponse:
        orchestrator = FakerOrchestrator(system_prompt=_SYSTEM_PROMPT)
        body = await orchestrator.chat(command.topic)
        subject = command.topic

        await self._email_sender.send(to=command.to, subject=subject, body=body)

        logger.info("[ComposeAndSendEmail] 발송 완료 | to=%s", command.to)
        return SendEmailResponse(success=True, to=command.to, subject=subject)
