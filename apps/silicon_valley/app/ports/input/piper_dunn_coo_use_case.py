from abc import ABC, abstractmethod
from silicon_valley.adapter.inbound.api.schemas.piper_dunn_coo_schema import DunnCooSchema
from silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooResponse

class DunnCooUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: DunnCooSchema) -> DunnCooResponse:
        pass
