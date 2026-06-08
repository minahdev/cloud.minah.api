from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.dependencies.passenger_isidor_couple_provider import get_passenger_isidor_couple_use_case
from titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleResponse
from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IsidorCoupleSchema

logger = logging.getLogger(__name__)

passenger_isidor_couple_router = APIRouter(prefix="/titanic/isidor", tags=["isidor"])


@passenger_isidor_couple_router.post("/myself", response_model=IsidorCoupleResponse)
async def upload_titanic_file(
    cal: IsidorCoupleUseCase = Depends(get_passenger_isidor_couple_use_case))-> IsidorCoupleResponse:
    
    return await cal.introduce_myself(
        IsidorCoupleSchema(
            id=8,
            name="Caledon Hockley",
            )
        )