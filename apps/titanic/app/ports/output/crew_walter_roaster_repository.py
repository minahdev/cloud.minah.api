from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery

class WalterRoasterRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: WalterRoasterQuery):
        pass