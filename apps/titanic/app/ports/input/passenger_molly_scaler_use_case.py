from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse
class MollyScalerUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: MollyScalerSchema)-> MollyScalerResponse:
        pass