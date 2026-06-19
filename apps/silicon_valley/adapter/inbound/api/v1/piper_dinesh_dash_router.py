from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from silicon_valley.app.ports.input.piper_dinesh_dash_use_case import DineshDashUseCase
from silicon_valley.dependencies.piper_dinesh_dash_provider import get_piper_dinesh_dash_use_case
from silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashResponse
from silicon_valley.adapter.inbound.api.schemas.piper_dinesh_dash_schema import DineshDashSchema

logger = logging.getLogger(__name__)

piper_dinesh_dash_router = APIRouter(prefix="/dinesh", tags=["dinesh"])


@piper_dinesh_dash_router.get("/myself", response_model=DineshDashResponse)
async def introduce_myself(
    dinesh: DineshDashUseCase = Depends(get_piper_dinesh_dash_use_case)) -> DineshDashResponse:

    return await dinesh.introduce_myself(
        DineshDashSchema(
            id=3,
            name="Dinesh Chugtai",
        )
    )
