from __future__ import annotations

from fastapi import APIRouter

from spam_filter.adapter.inbound.api.v1.spam_filter_router import spam_filter_router as _spam_filter_v1_router

spam_filter_router = APIRouter()
spam_filter_router.include_router(_spam_filter_v1_router)

__all__ = ["spam_filter_router"]
