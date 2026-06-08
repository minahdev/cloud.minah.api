from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository

import logging

logger = logging.getLogger(__name__)

class LoweBoatPgRepository(LoweBoatRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: LoweBoatQuery) -> LoweBoatResponse:
        
        '''로어 보트의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[LoweBoatPgRepository] 🍔introduce_myself 진입 | request_data={query}")
        
        response: LoweBoatResponse = LoweBoatResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )

        logger.info(f"[LoweBoatPgRepository] 🍔introduce_myself 종료 | response_data={response}")

        return response