from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse

class SmithCaptainUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: SmithCaptainSchema)-> SmithCaptainResponse:
        pass