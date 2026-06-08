from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse

class CalTesterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: CalTesterSchema)-> CalTesterResponse:
        pass