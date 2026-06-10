from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_crew_smith_captain_use_case
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema

logger = logging.getLogger(__name__)

crew_smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])



@crew_smith_captain_router.post("/", response_model=SmithCaptainResponse)
async def chat(
    smith: SmithCaptainUseCase = Depends(get_crew_smith_captain_use_case)
    )-> SmithCaptainResponse:
    return None
    
    



@crew_smith_captain_router.get("/myself", response_model=SmithCaptainResponse)
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_crew_smith_captain_use_case))-> SmithCaptainResponse:
    
    return await smith.introduce_myself(
        SmithCaptainSchema(
            id=5,
            name="Edward John Smith",
        )
    )



    