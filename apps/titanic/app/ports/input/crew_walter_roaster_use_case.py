from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse

class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def get_train_set(self)->WalterRoasterResponse:
        '''월터가 DB에서 train set 만 가져오는 메소드'''

    @abstractmethod
    async def get_test_set(self)->WalterRoasterResponse:
        '''월터가 DB에서 test set 만 가져오는 메소드'''

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema)->WalterRoasterResponse:
        pass

