from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema

logger = logging.getLogger(__name__)

passenger_jack_trainer_router = APIRouter(prefix="/jack", tags=["jack"])


@passenger_jack_trainer_router.get("/myself", response_model=JackTrainerResponse)
async def introduce_myself(
    jack: JackTrainerUseCase = Depends(get_jack_trainer))-> JackTrainerResponse:
    
    return await jack.introduce_myself(
        JackTrainerSchema(
            id=9,
            name="Jack Dawson",
            )
        )