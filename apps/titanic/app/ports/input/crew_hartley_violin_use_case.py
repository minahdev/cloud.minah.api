from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema

class HartleyViolinUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: HartleyViolinSchema):
        pass
