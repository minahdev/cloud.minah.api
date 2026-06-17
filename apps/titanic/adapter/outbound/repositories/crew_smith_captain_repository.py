from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainQuery, SmithCaptainChatCommand
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort

import logging

logger = logging.getLogger(__name__)

class SmithCaptainRepository(SmithCaptainPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        
        '''스미스 캡틴의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[SmithCaptainPgRepository] 🍔introduce_myself 진입 | request_data={query}")
        
        response: SmithCaptainResponse = SmithCaptainResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )

        return response

    async def chat(self, command: SmithCaptainChatCommand) -> SmithCaptainResponse:
        logger.info(f"[SmithCaptainPgRepository] 💬chat 진입 | message={command.message}")

        return SmithCaptainResponse(
            id=0,
            name="SmithCaptain",
            reply=f"[Smith] '{command.message}' 수신됨"
        )