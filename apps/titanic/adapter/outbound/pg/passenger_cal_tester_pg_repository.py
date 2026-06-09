from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository

import logging

logger = logging.getLogger(__name__)

class CalTesterPgRepository(CalTesterRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        
        '''칼의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[CalTesterPgRepository] 🌭introduce_myself 진입 | request_data={query}")
        
        response: CalTesterResponse = CalTesterResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )

        return response