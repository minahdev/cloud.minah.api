from __future__ import annotations

import logging

from comm_agent.app.dtos.email_send_dto import SendEmailCommand, SendEmailResponse
from comm_agent.app.ports.input.email_send_use_case import ComposeAndSendEmailUseCase

from star_craft.domain.ontology.communication.email_template import get_email_spec
from star_craft.domain.ontology.communication.email_type import EmailType

logger = logging.getLogger(__name__)


class ComposeEmailOrchestrator:
    """Hub 오케스트레이터 — 주문을 받아 온톨로지로 규격을 정하고 comm_agent에 위임한다.

    - 온톨로지(지식)는 읽기만 한다 → 규격 결정은 여기(라우팅/오케스트레이션).
    - 실제 작성·발송 로직은 갖지 않는다 → comm_agent 포트로 위임 (Hub→Spoke port).
    """

    def __init__(self, email_use_case: ComposeAndSendEmailUseCase) -> None:
        self._email_use_case = email_use_case

    async def compose_and_send(
        self,
        to: str,
        topic: str,
        email_type: EmailType,
        subject: str = "",
        sender_name: str = "",
    ) -> SendEmailResponse:
        logger.info(
            "[1/3][star_craft 입구] 주문 수신 | to=%s | topic=%s | email_type=%s -> 온톨로지 조회",
            to,
            topic,
            email_type.value,
        )
        spec = get_email_spec(email_type)
        logger.info(
            "[2.5/3][star_craft] 온톨로지 규격 확정 -> comm_agent 포트로 위임 | label=%s",
            spec.type_label,
        )
        command = SendEmailCommand(
            to=to,
            topic=topic,
            subject=subject,
            sender_name=sender_name,
            type_label=spec.type_label,
            tone=spec.tone,
            required_elements=spec.required_elements,
        )
        # 텔레그램 업무보고는 n8n 이메일 워크플로(Gmail → Telegram)에서 처리한다.
        return await self._email_use_case.compose_and_send(command)
