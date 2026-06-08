from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository

import logging

logger = logging.getLogger(__name__)

class AndrewsArchitectPgRepository(AndrewsArchitectRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: AndrewsArchitectQuery) -> AndrewsArchitectResponse:
        
        '''앤드류의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[AndrewsArchitectPgRepository] 🍕introduce_myself 진입 | request_data={query}")
        
        response: AndrewsArchitectResponse = AndrewsArchitectResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )

        logger.info(f"[AndrewsArchitectPgRepository] 🍕introduce_myself 종료 | response_data={response}")

        return response