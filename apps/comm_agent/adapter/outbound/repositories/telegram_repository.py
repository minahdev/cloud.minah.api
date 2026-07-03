from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


from comm_agent.app.dtos.telegram_dto import TelegramResponse, TelegramSendQuery
from comm_agent.app.ports.output.telegram_port import TelegramSenderPort

import logging

logger = logging.getLogger(__name__)

class TelegramRepository(TelegramSenderPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: TelegramSendQuery) -> TelegramResponse:

        '''텔레그램의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[TelegramRepository] 🍿introduce_myself 진입 | request_data={query}")

        response: TelegramResponse = TelegramResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response