from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse, JackTrainerQuery

class JackTrainerRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: JackTrainerQuery)-> JackTrainerResponse:
        pass
