from abc import ABC, abstractmethod
from silicon_valley.adapter.inbound.api.schemas.piper_hendricks_ceo_schema import HendricksCeoSchema
from silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoResponse

class HendricksCeoUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: HendricksCeoSchema) -> HendricksCeoResponse:
        pass
