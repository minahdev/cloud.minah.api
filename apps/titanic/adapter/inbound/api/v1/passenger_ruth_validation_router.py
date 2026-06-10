from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from titanic.dependencies.passenger_ruth_validation_provider import get_passenger_ruth_survivor_use_case
from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationResponse
from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema

logger = logging.getLogger(__name__)

passenger_ruth_validation_router = APIRouter(prefix="/ruth", tags=["ruth"])


@passenger_ruth_validation_router.get("/myself", response_model=RuthValidationResponse)
async def introduce_myself(
    ruth: RuthValidationUseCase = Depends(get_passenger_ruth_survivor_use_case))-> RuthValidationResponse:
    
    return await ruth.introduce_myself(
        RuthValidationSchema(
            id=12,
            name="Ruth DeWitt Bukater",
            )
        )