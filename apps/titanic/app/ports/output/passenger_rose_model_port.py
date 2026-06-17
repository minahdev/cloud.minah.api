from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse, RoseModelQuery, TrainingData

class RoseModelPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        pass

    @abstractmethod
    async def get_training_data(self) -> TrainingData:
        pass
