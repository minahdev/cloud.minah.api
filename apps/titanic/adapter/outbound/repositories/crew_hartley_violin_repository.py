from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort

import logging

logger = logging.getLogger(__name__)

class HartleyViolinRepository(HartleyViolinPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: HartleyViolinQuery) -> HartleyViolinResponse:
        
        '''하트리의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[HartleyViolinPgRepository] 🍔introduce_myself 진입 | request_data={query}")
        
        response: HartleyViolinResponse = HartleyViolinResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )

        return response