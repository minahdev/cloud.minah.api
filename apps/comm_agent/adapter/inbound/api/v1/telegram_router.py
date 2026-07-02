from __future__ import annotations

import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException

from comm_agent.adapter.inbound.api.schemas.telegram_schema import (
    TelegramIntroduceSchema,
    TelegramSendSchema,
)
from comm_agent.app.dtos.email_send_dto import IntroduceResponse
from comm_agent.app.dtos.telegram_dto import TelegramSendCommand, TelegramSendResponse
from comm_agent.app.ports.input.telegram_use_case import TelegramUseCase
from comm_agent.dependencies.telegram_provider import get_telegram_use_case

logger = logging.getLogger(__name__)

telegram_router = APIRouter(prefix="/comm_agent/telegram", tags=["comm_agent_telegram"])


@telegram_router.post("/send", response_model=TelegramSendResponse)
async def send_telegram(
    schema: TelegramSendSchema,
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
) -> TelegramSendResponse:
    """주제로 메시지를 생성해 텔레그램으로 발송한다."""
    try:
        return await use_case.send_message(
            TelegramSendCommand(chat_id=schema.chat_id, topic=schema.topic)
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"텔레그램 발송 오류: {e.response.status_code}",
        ) from e
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e).strip() or "텔레그램 발송에 실패했습니다.",
        ) from e


@telegram_router.get("/myself", response_model=IntroduceResponse)
async def introduce_myself(
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
) -> IntroduceResponse:
    """Telegram 채널 자기소개."""
    return await use_case.introduce_myself(
        TelegramIntroduceSchema(
            id=8,
            name="Telegram Agent",
        )
    )
