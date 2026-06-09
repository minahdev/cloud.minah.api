from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse, RoseModelQuery

class RoseModelRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: RoseModelQuery)-> RoseModelResponse:
        pass
