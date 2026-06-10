from fastapi import APIRouter
from fastapi import Depends

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_crew_walter_roaster_use_case
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse

import logging
logger = logging.getLogger(__name__)


crew_walter_roaster_router = APIRouter(prefix="/walter", tags=["walter"])

@crew_walter_roaster_router.get("/myself", response_model=WalterRoasterResponse)
async def introduce_myself(
    walter : WalterRoasterUseCase = Depends(get_crew_walter_roaster_use_case)) -> WalterRoasterResponse:

    return await walter.introduce_myself(
        WalterRoasterSchema(
            id=6,
            name="Walter Roaster",
            )
        )

    