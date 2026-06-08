from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse

class LoweBoatUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: LoweBoatSchema)-> LoweBoatResponse:
        pass