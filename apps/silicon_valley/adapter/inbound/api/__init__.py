from __future__ import annotations

from fastapi import APIRouter

from silicon_valley.adapter.inbound.api.v1.piper_hendricks_ceo_router import piper_hendricks_ceo_router
from silicon_valley.adapter.inbound.api.v1.piper_bighetti_hr_router import piper_bighetti_hr_router
from silicon_valley.adapter.inbound.api.v1.piper_dinesh_dash_router import piper_dinesh_dash_router
from silicon_valley.adapter.inbound.api.v1.piper_dunn_coo_router import piper_dunn_coo_router
from silicon_valley.adapter.inbound.api.v1.piper_gilfoyle_sys_router import piper_gilfoyle_sys_router

silicon_valley_router = APIRouter(prefix="/silicon-valley", tags=["silicon-valley"])
silicon_valley_router.include_router(piper_hendricks_ceo_router)
silicon_valley_router.include_router(piper_bighetti_hr_router)
silicon_valley_router.include_router(piper_dinesh_dash_router)
silicon_valley_router.include_router(piper_dunn_coo_router)
silicon_valley_router.include_router(piper_gilfoyle_sys_router)

__all__ = ["silicon_valley_router"]
