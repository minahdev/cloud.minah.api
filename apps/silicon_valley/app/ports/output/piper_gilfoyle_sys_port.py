from abc import ABC, abstractmethod
from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import GilfoyleSysQuery, GilfoyleSysResponse

class GilfoyleSysPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: GilfoyleSysQuery) -> GilfoyleSysResponse:
        pass
