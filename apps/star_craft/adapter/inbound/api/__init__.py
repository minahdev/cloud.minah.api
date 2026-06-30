from __future__ import annotations

from fastapi import APIRouter

from star_craft.adapter.inbound.api.v1.star_craft_router import star_craft_router as _star_craft_v1_router

star_craft_router = APIRouter()
star_craft_router.include_router(_star_craft_v1_router)

__all__ = ["star_craft_router"]
