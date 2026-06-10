from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.dependencies.crew_andrews_architect_provider import get_crew_andrews_architect_use_case
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse
from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema

logger = logging.getLogger(__name__)

crew_andrews_architect_router = APIRouter(prefix="/andrews", tags=["andrews"])


@crew_andrews_architect_router.get("/myself", response_model=AndrewsArchitectResponse)
async def introduce_myself(
    andrews: AndrewsArchitectUseCase = Depends(get_crew_andrews_architect_use_case))-> AndrewsArchitectResponse:
    
    return await andrews.introduce_myself(
        AndrewsArchitectSchema(
            id=2,
            name="Thomas Andrews",
            )
        )