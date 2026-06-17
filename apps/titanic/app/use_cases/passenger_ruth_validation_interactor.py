from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import (
    RuthValidationSchema
)
from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationResponse, RuthValidationQuery
from titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from titanic.app.ports.output.passenger_ruth_validation_port import RuthValidationPort

import logging

logger = logging.getLogger(__name__)

class RuthValidationInteractor(RuthValidationUseCase):

    def __init__(self, repository: RuthValidationPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        
        return await self._repository.introduce_myself(RuthValidationQuery(
            id= schema.id,
            name= schema.name
        ))