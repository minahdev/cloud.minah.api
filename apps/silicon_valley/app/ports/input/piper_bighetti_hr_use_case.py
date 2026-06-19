from abc import ABC, abstractmethod
from silicon_valley.adapter.inbound.api.schemas.piper_bighetti_hr_schema import BighettiHrSchema
from silicon_valley.app.dtos.piper_bighetti_hr_dto import BighettiHrResponse

class BighettiHrUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: BighettiHrSchema) -> BighettiHrResponse:
        pass
