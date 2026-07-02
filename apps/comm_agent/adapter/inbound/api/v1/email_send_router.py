from __future__ import annotations

import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException

from comm_agent.adapter.inbound.api.schemas.send_email_schema import (
    ComposeEmailIntroduceSchema,
    SendEmailSchema,
)
from comm_agent.app.dtos.email_send_dto import (
    IntroduceResponse,
    SendEmailCommand,
    SendEmailResponse,
)
from comm_agent.app.ports.input.email_send_use_case import ComposeAndSendEmailUseCase
from comm_agent.dependencies.email_send_provider import (
    get_compose_and_send_email_use_case,
)

logger = logging.getLogger(__name__)

comm_agent_router = APIRouter(prefix="/comm_agent", tags=["comm_agent"])


@comm_agent_router.post("/send", response_model=SendEmailResponse)
async def send_email(
    schema: SendEmailSchema,
    use_case: ComposeAndSendEmailUseCase = Depends(get_compose_and_send_email_use_case),
) -> SendEmailResponse:
    """주제로 본문을 생성해 입력한 이메일 주소로 발송한다."""
    try:
        return await use_case.compose_and_send(
            SendEmailCommand(to=schema.email, topic=schema.topic)
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"메일 발송(n8n) 오류: {e.response.status_code}",
        ) from e
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e).strip() or "메일 발송에 실패했습니다.",
        ) from e


@comm_agent_router.get("/myself", response_model=IntroduceResponse)
async def introduce_myself(
    use_case: ComposeAndSendEmailUseCase = Depends(get_compose_and_send_email_use_case),
) -> IntroduceResponse:
    """Comm Agent 자기소개."""
    return await use_case.introduce_myself(
        ComposeEmailIntroduceSchema(
            id=3,
            name="Comm Agent",
        )
    )
