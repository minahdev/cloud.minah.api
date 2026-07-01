from __future__ import annotations

import logging

from comm_agent.app.dtos.email_send_dto import IntroduceResponse
from comm_agent.app.ports.input.discord_use_case import DiscordUseCase

logger = logging.getLogger(__name__)


class DiscordInteractor(DiscordUseCase):
    async def introduce_myself(self, id: int, name: str) -> IntroduceResponse:
        logger.info("[Discord] introduce_myself 진입 | id=%s name=%s", id, name)
        return IntroduceResponse(
            id=id,
            name=name,
            answer=f"안녕하세요, 저는 '{name}'입니다. 디스코드 채널로 메시지를 보내는 통신 비서예요.",
        )
