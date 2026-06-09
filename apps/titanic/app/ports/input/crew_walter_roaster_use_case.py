from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse

class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema)->WalterRoasterResponse:
        pass