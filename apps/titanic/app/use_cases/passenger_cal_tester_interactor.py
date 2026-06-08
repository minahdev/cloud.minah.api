from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import (
    CalTesterSchema,
)
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

import logging

logger = logging.getLogger(__name__)

class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: SmithCaptainRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        
        return await self._repository.introduce_myself(CalTesterQuery(
            id= schema.id,
            name= schema.name
        ))