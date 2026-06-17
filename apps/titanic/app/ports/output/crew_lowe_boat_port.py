from abc import ABC, abstractmethod

from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse, LoweBoatQuery

class LoweBoatPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: LoweBoatQuery)->LoweBoatResponse:
        pass