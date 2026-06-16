from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.dependencies.passenger_cal_tester_provider import get_passenger_cal_tester_use_case
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse
from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema

logger = logging.getLogger(__name__)

passenger_cal_tester_router = APIRouter(prefix="/cal", tags=["cal"])


@passenger_cal_tester_router.get("/myself", response_model=CalTesterResponse)
async def introduce_myself(
    cal: CalTesterUseCase = Depends(get_passenger_cal_tester_use_case)) -> CalTesterResponse:
    return await cal.introduce_myself(CalTesterSchema(id=7, name="Caledon Hockley"))


@passenger_cal_tester_router.get("/ranking")
async def get_model_ranking(
    cal: CalTesterUseCase = Depends(get_passenger_cal_tester_use_case)):
    return await cal.test_model(test_set=None)