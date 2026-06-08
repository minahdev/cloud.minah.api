from abc import ABC, abstractmethod

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse

class AndrewsArchitectRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: AndrewsArchitectQuery)->AndrewsArchitectResponse:
        pass