from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse

class CalTesterRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: CalTesterQuery)-> CalTesterResponse:
        pass
