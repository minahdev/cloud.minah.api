from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from comm_agent.adapter.inbound.api.schemas.receive_mail_schema import (
    ReceivedMailIntroduceSchema,
    ReceivedMailViewSchema,
    ReceiveMailSchema,
)
from comm_agent.app.dtos.received_mail_dto import (
    ReceivedMailCommand,
    ReceivedMailResponse,
)
from comm_agent.app.ports.input.push_use_case import PushUseCase
from comm_agent.app.ports.input.received_mail_use_case import ReceiveMailUseCase
from comm_agent.dependencies.push_provider import get_push_use_case
from comm_agent.dependencies.received_mail_provider import get_receive_mail_use_case

logger = logging.getLogger(__name__)

receive_router = APIRouter(prefix="/comm_agent/receive", tags=["comm_agent_receive"])


@receive_router.post("/gmail")
async def receive_gmail(
    schema: ReceiveMailSchema,
    use_case: ReceiveMailUseCase = Depends(get_receive_mail_use_case),
    push_use_case: PushUseCase = Depends(get_push_use_case),
) -> dict:
    """n8n이 Gmail에서 감지한 새 메일을 저장하고 푸시 알림을 보낸다."""
    mail_id = await use_case.save_incoming(
        ReceivedMailCommand(sender=schema.from_, subject=schema.subject, body=schema.body)
    )

    #여기에 들어오면 로그를 작성해줘.
    #여기에 들어오면 텔레그램으로 전송해줘.



    # 푸시 실패해도 메일 수신(n8n) 자체는 성공 처리
    try:
        await push_use_case.notify_all(title="새 메일", body=f"{schema.from_} · {schema.subject}")
    except Exception as e:  # noqa: BLE001
        logger.warning("[Push] 알림 발송 실패(무시): %s", e)
    return {"ok": True, "id": mail_id}


@receive_router.get("", response_model=list[ReceivedMailViewSchema])
async def list_received_mails(
    use_case: ReceiveMailUseCase = Depends(get_receive_mail_use_case),
) -> list[ReceivedMailViewSchema]:
    """저장된 수신 메일을 최신순으로 돌려준다."""
    views = await use_case.list_received()
    return [
        ReceivedMailViewSchema(
            id=v.id,
            sender=v.sender,
            subject=v.subject,
            body=v.body,
            received_at=v.received_at,
        )
        for v in views
    ]


@receive_router.get("/myself", response_model=ReceivedMailResponse)
async def introduce_myself(
    use_case: ReceiveMailUseCase = Depends(get_receive_mail_use_case),
) -> ReceivedMailResponse:
    return await use_case.introduce_myself(
        ReceivedMailIntroduceSchema(
            id=7,
            name="수신 메일 (Received Mail)",
        )
    )
