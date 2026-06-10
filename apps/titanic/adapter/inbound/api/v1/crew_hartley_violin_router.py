import logging

from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.dependencies.crew_hartley_violin_provider import get_crew_hartley_violin_use_case
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse
from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema

logger = logging.getLogger(__name__)

crew_hartley_violin_router = APIRouter(prefix="/hartley", tags=["hartley"])


@crew_hartley_violin_router.get("/myself", response_model=HartleyViolinResponse)
async def introduce_myself(
    hartley: HartleyViolinUseCase = Depends(get_crew_hartley_violin_use_case))-> HartleyViolinResponse:
    
    return await hartley.introduce_myself(
        HartleyViolinSchema(
            id=3,
            name="Wallace Hartley",
            )
        )