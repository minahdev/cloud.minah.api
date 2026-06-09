from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse, MollyScalerQuery

class MollyScalerRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: MollyScalerQuery)-> MollyScalerResponse:
        pass
