from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from silicon_valley.app.ports.input.piper_gilfoyle_sys_use_case import GilfoyleSysUseCase
from silicon_valley.dependencies.piper_gilfoyle_sys_provider import get_piper_gilfoyle_sys_use_case
from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import GilfoyleSysResponse
from silicon_valley.adapter.inbound.api.schemas.piper_gilfoyle_sys_schema import GilfoyleSysSchema

logger = logging.getLogger(__name__)

piper_gilfoyle_sys_router = APIRouter(prefix="/gilfoyle", tags=["gilfoyle"])


@piper_gilfoyle_sys_router.get("/myself", response_model=GilfoyleSysResponse)
async def introduce_myself(
    gilfoyle: GilfoyleSysUseCase = Depends(get_piper_gilfoyle_sys_use_case)) -> GilfoyleSysResponse:

    return await gilfoyle.introduce_myself(
        GilfoyleSysSchema(
            id=5,
            name="Bertram Gilfoyle",
        )
    )
