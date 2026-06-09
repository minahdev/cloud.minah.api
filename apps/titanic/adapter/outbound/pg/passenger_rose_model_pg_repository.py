from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse, RoseModelQuery
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

import logging

logger = logging.getLogger(__name__)

class RoseModelPgRepository(RoseModelRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        
        ''' 로즈의 자기 소개 레포지토리 구현 메소드 '''

        logger.info(f"[RoseModelPgRepository] 🧇introduce_myself 진입 | request_data={query}")
        
        response: RoseModelResponse = RoseModelResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )

        logger.info(f"[RoseModelPgRepository] 🧇introduce_myself 종료 | response_data={response}")

        return response