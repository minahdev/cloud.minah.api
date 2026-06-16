from abc import ABC, abstractmethod
from typing import Any
from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse

class CalTesterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: CalTesterSchema)-> CalTesterResponse:
        pass

    @abstractmethod
    async def test_model(self,test_set) -> dict[str, Any]:
        '''잭이 훈련시킨 모델을 1위부터 10위까지 나열하는 메소드... '''