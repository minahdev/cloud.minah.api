from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Depends

from comm_agent.adapter.inbound.api.schemas.push_schema import (
    PushIntroduceSchema,
    PushSubscribeSchema,
    VapidPublicKeyResponse,
)
from comm_agent.app.dtos.push_dto import PushResponse, PushSubscriptionCommand
from comm_agent.app.ports.input.push_use_case import PushUseCase
from comm_agent.dependencies.push_provider import get_push_use_case

logger = logging.getLogger(__name__)

push_router = APIRouter(prefix="/comm_agent/push", tags=["comm_agent_push"])


@push_router.get("/vapid-public-key", response_model=VapidPublicKeyResponse)
async def vapid_public_key() -> VapidPublicKeyResponse:
    """브라우저 구독에 필요한 VAPID 공개키를 돌려준다."""
    return VapidPublicKeyResponse(public_key=os.getenv("VAPID_PUBLIC_KEY", ""))


@push_router.post("/subscribe")
async def subscribe(
    schema: PushSubscribeSchema,
    use_case: PushUseCase = Depends(get_push_use_case),
) -> dict:
    """브라우저 푸시 구독을 저장한다."""
    await use_case.subscribe(
        PushSubscriptionCommand(
            endpoint=schema.endpoint,
            p256dh=schema.keys.p256dh,
            auth=schema.keys.auth,
        )
    )
    return {"ok": True}


@push_router.get("/myself", response_model=PushResponse)
async def introduce_myself(
    use_case: PushUseCase = Depends(get_push_use_case),
) -> PushResponse:
    return await use_case.introduce_myself(
        PushIntroduceSchema(
            id=6,
            name="웹 푸시 (Push)",
        )
    )
