from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.dtos.passenger_rose_model_dto import TrainingData

class CalTesterPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        pass

    @abstractmethod
    async def get_training_data(self) -> TrainingData:
        pass
