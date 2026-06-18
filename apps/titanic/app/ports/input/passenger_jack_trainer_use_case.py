from abc import ABC, abstractmethod
from typing import Any
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse

class JackTrainerUseCase(ABC):

    @abstractmethod
    async def train_model(self, X_train: list[list[float]], y_label: list[int]) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''

    @abstractmethod
    async def analyze_jack_dawson(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        ...