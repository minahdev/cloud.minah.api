from abc import ABC, abstractmethod
from silicon_valley.adapter.inbound.api.schemas.piper_gilfoyle_sys_schema import GilfoyleSysSchema
from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import GilfoyleSysResponse

class GilfoyleSysUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: GilfoyleSysSchema) -> GilfoyleSysResponse:
        pass
