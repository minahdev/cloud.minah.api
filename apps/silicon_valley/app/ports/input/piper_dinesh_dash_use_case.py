from abc import ABC, abstractmethod
from silicon_valley.adapter.inbound.api.schemas.piper_dinesh_dash_schema import DineshDashSchema
from silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashResponse

class DineshDashUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: DineshDashSchema) -> DineshDashResponse:
        pass
