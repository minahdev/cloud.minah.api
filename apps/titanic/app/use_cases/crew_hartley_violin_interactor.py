from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import (
    HartleyViolinSchema,
)
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository

import logging

logger = logging.getLogger(__name__)

class HartleyViolinInteractor(HartleyViolinUseCase):

    def __init__(self, repository: HartleyViolinRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        
        return await self._repository.introduce_myself(HartleyViolinQuery(
            id= schema.id,
            name= schema.name
        ))