from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    SmithCaptainSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainQuery
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

import logging

logger = logging.getLogger(__name__)

class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        
        return await self._repository.introduce_myself(SmithCaptainQuery(
            id= schema.id,
            name= schema.name
        ))