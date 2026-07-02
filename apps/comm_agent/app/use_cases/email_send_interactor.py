from __future__ import annotations

import logging

from comm_agent.adapter.inbound.api.schemas.send_email_schema import (
    ComposeEmailIntroduceSchema,
)
from comm_agent.app.dtos.email_send_dto import (
    IntroduceResponse,
    SendEmailCommand,
    SendEmailResponse,
)
from comm_agent.app.ports.input.email_send_use_case import ComposeAndSendEmailUseCase
from comm_agent.app.ports.output.email_send_port import EmailSenderPort
from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator

logger = logging.getLogger(__name__)


def _build_system_prompt(command: SendEmailCommand) -> str:
    """Hub 온톨로지가 넘긴 규격(유형·톤·필수요소)으로 작성 지시문을 만든다."""
    label = command.type_label or "일반"
    tone = command.tone or "정중하고 간결한"
    parts = [
        f"너는 '{label}' 유형의 한국어 이메일 본문을 작성하는 비서다.",
        f"{tone} 말투로 작성해라.",
    ]
    if command.required_elements:
        parts.append("다음 요소를 반드시 포함해라: " + ", ".join(command.required_elements) + ".")
    parts.append("인사말과 맺음말을 포함하고, 제목이나 머리말 없이 본문만 출력해라.")
    if command.sender_name.strip():
        parts.append(
            f"맺음말 서명은 반드시 '{command.sender_name.strip()} 드림'으로 끝내라. "
            "'[당신의 이름]' 같은 자리표시자를 절대 쓰지 마라."
        )
    else:
        parts.append("'[당신의 이름]' 같은 자리표시자를 절대 쓰지 말고, 서명 줄은 생략해라.")
    return " ".join(parts)


class ComposeAndSendEmailInteractor(ComposeAndSendEmailUseCase):
    def __init__(self, email_sender: EmailSenderPort) -> None:
        self._email_sender = email_sender

    async def compose_and_send(self, command: SendEmailCommand) -> SendEmailResponse:
        logger.info(
            "[3/3][comm_agent] 온톨로지 규격 수신 | label=%s | tone=%s | 필수요소=%s",
            command.type_label or "(없음)",
            command.tone or "(없음)",
            list(command.required_elements),
        )
        system_prompt = _build_system_prompt(command)
        logger.info("[3/3][comm_agent] 규격으로 생성된 exaone 지시문: %s", system_prompt)

        orchestrator = FakerOrchestrator(system_prompt=system_prompt)
        body = await orchestrator.chat(command.topic)
        # 제목은 입력한 subject 사용. 비어 있으면 topic으로 폴백.
        subject = command.subject.strip() or command.topic

        await self._email_sender.send(to=command.to, subject=subject, body=body)

        logger.info("[comm_agent] exaone 작성 완료 -> 발송 완료 | to=%s", command.to)
        return SendEmailResponse(success=True, to=command.to, subject=subject)

    async def introduce_myself(self, schema: ComposeEmailIntroduceSchema) -> IntroduceResponse:
        logger.info(
            "[comm_agent] introduce_myself 진입 | id=%s name=%s", schema.id, schema.name
        )
        return IntroduceResponse(
            id=schema.id,
            name=schema.name,
            answer=f"안녕하세요, 저는 '{schema.name}'입니다. 받는 사람과 주제를 주시면 이메일 본문을 작성해 발송하는 통신 비서예요.",
        )
