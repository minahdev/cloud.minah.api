from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema

class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema):
        pass