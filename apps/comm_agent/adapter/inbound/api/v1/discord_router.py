from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from comm_agent.adapter.inbound.api.schemas.discord_schema import DiscordIntroduceSchema
from comm_agent.app.dtos.email_send_dto import IntroduceResponse
from comm_agent.app.ports.input.discord_use_case import DiscordUseCase
from comm_agent.dependencies.discord_provider import get_discord_use_case

logger = logging.getLogger(__name__)

discord_router = APIRouter(prefix="/comm_agent/discord", tags=["comm_agent_discord"])


@discord_router.get("/myself", response_model=IntroduceResponse)
async def introduce_myself(
    use_case: DiscordUseCase = Depends(get_discord_use_case),
) -> IntroduceResponse:
    """Discord 채널 자기소개."""
    return await use_case.introduce_myself(
        DiscordIntroduceSchema(
            id=2,
            name="Discord Agent",
        )
    )
