from abc import ABC, abstractmethod

from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse

class HartleyViolinPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: HartleyViolinQuery)->HartleyViolinResponse:
        pass
