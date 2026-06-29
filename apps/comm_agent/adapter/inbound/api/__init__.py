from __future__ import annotations

from fastapi import APIRouter

from comm_agent.adapter.inbound.api.v1.comm_agent_router import comm_agent_router as _comm_agent_v1_router

comm_agent_router = APIRouter()
comm_agent_router.include_router(_comm_agent_v1_router)

__all__ = ["comm_agent_router"]
