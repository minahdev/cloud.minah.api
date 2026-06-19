from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from silicon_valley.app.ports.input.piper_hendricks_ceo_use_case import HendricksCeoUseCase
from silicon_valley.dependencies.piper_hendricks_ceo_provider import get_piper_hendricks_ceo_use_case
from silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoResponse
from silicon_valley.adapter.inbound.api.schemas.piper_hendricks_ceo_schema import HendricksCeoSchema

logger = logging.getLogger(__name__)

piper_hendricks_ceo_router = APIRouter(prefix="/hendricks", tags=["hendricks"])


@piper_hendricks_ceo_router.get("/myself", response_model=HendricksCeoResponse)
async def introduce_myself(
    hendricks: HendricksCeoUseCase = Depends(get_piper_hendricks_ceo_use_case)) -> HendricksCeoResponse:

    return await hendricks.introduce_myself(
        HendricksCeoSchema(
            id=1,
            name="Richard Hendricks",
        )
    )
