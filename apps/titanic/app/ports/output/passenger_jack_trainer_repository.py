from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse, JackTrainerQuery
from titanic.app.dtos.passenger_rose_model_dto import TrainingData

class JackTrainerRepository(ABC):

    @abstractmethod
    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        pass

    @abstractmethod
    async def get_training_data(self) -> TrainingData:
        pass
