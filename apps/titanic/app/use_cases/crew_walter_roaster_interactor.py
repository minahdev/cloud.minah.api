from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import (
    WalterRoasterSchema,
)
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger(__name__)


class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self, repository: WalterRoasterRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        
        return await self._repository.introduce_myself(WalterRoasterQuery(
            id= schema.id,
            name= schema.name
        ))
