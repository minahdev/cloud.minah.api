from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import (
    RoseModelSchema
)
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse, RoseModelQuery
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

import logging

logger = logging.getLogger(__name__)

class RoseModelInteractor(RoseModelUseCase):

    def __init__(self, repository: RoseModelRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        
        return await self._repository.introduce_myself(RoseModelQuery(
            id= schema.id,
            name= schema.name
        ))