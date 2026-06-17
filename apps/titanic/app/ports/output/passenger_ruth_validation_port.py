from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse

class RuthValidationPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: RuthValidationQuery)-> RuthValidationResponse:
        pass
