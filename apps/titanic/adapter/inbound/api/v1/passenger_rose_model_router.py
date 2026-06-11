from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.dependencies.passenger_rose_model_provider import get_rose_model
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse
from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema

logger = logging.getLogger(__name__)

passenger_rose_model_router = APIRouter(prefix="/rose", tags=["rose"])


@passenger_rose_model_router.get("/myself", response_model=RoseModelResponse)
async def introduce_myself(
    rose: RoseModelUseCase = Depends(get_rose_model))-> RoseModelResponse:
    
    return await rose.introduce_myself(
        RoseModelSchema(
            id=11,
            name="Rose DeWitt Bukater",
            )
        )