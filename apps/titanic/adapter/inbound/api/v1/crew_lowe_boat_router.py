from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.dependencies.crew_lowe_boat_provider import get_crew_lowe_boat_use_case
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse
from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema

logger = logging.getLogger(__name__)

crew_lowe_boat_router = APIRouter(prefix="/lowe", tags=["lowe"])


@crew_lowe_boat_router.get("/myself", response_model=LoweBoatResponse)
async def introduce_myself(
    lowe: LoweBoatUseCase = Depends(get_crew_lowe_boat_use_case))-> LoweBoatResponse:
    
    return await lowe.introduce_myself(
        LoweBoatSchema(
            id=4,
            name="Harold Lowe",
            )
        )