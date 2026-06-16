from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema, RosePredictSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse, PredictResponse

class RoseModelUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        pass

    @abstractmethod
    async def predict_survival(self, schema: RosePredictSchema) -> PredictResponse:
        pass