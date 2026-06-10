from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.dependencies.passenger_molly_scaler_provider import get_passenger_molly_scaler_use_case
from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse
from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema

logger = logging.getLogger(__name__)

passenger_molly_scaler_router = APIRouter(prefix="/molly", tags=["molly"])


@passenger_molly_scaler_router.get("/myself", response_model=MollyScalerResponse)
async def introduce_myself(
    molly: MollyScalerUseCase = Depends(get_passenger_molly_scaler_use_case))-> MollyScalerResponse:
    
    return await molly.introduce_myself(
        MollyScalerSchema(
            id=10,
            name="Molly Brown",
            )
        )