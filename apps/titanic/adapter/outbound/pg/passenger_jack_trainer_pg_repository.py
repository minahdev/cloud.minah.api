from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

import logging

logger = logging.getLogger(__name__)

class JackTrainerPgRepository(JackTrainerRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        
        '''잭의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[JackTrainerPgRepository] 🥓introduce_myself 진입 | request_data={query}")
        
        response: JackTrainerResponse = JackTrainerResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )


        return response