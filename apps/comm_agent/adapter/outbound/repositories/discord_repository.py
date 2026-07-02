from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from comm_agent.app.dtos.discord_dto import DiscordQuery, DiscordResponse
from comm_agent.app.ports.output.discord_port import DiscordPort

import logging

logger = logging.getLogger(__name__)

class DiscordRepository(DiscordPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: DiscordQuery) -> DiscordResponse:
        
        '''디스코드의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[DiscordRepository] 🍿introduce_myself 진입 | request_data={query}")
        
        response: DiscordResponse = DiscordResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response