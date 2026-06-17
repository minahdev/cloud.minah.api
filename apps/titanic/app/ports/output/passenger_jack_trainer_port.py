from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse, JackTrainerQuery
from titanic.app.dtos.passenger_rose_model_dto import TrainingData

class JackTrainerPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        '''잭 트레이너의 자기 소개 레포지토리 추상 메소드'''
        pass

    @abstractmethod
    async def get_training_data(self) -> TrainingData:
        pass
