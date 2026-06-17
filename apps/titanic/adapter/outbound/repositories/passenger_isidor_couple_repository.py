from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleQuery, IsidorCoupleResponse
from titanic.app.ports.output.passenger_isidor_couple_port import IsidorCouplePort

import logging

logger = logging.getLogger(__name__)

class IsidorCoupleRepository(IsidorCouplePort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: IsidorCoupleQuery) -> IsidorCoupleResponse:
        
        '''이시도르의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[IsidorCouplePgRepository] 🍿introduce_myself 진입 | request_data={query}")
        
        response: IsidorCoupleResponse = IsidorCoupleResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response