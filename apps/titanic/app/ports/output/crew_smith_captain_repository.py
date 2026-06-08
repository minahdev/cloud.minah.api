from abc import ABC, abstractmethod

from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainQuery

class SmithCaptainRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: SmithCaptainQuery)->SmithCaptainResponse:
        pass