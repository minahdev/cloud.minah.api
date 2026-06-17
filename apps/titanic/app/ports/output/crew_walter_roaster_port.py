from abc import ABC, abstractmethod

import pandas as pd

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse

class WalterRoasterPort(ABC):
    '''월터의 승객 명단 관리 저장소'''

    @abstractmethod
    async def get_train_set(self) -> pd.DataFrame:
        ''' Survived 컬럼이 있는 데이터 전체를 데이터프레임으로 반환하는 메소드'''
        pass

    @abstractmethod
    async def get_test_set(self) -> pd.DataFrame:
        '''Survived 컬럼이 없는 데이터 전체를 데이터프레임으로 반환하는 메소드'''
        pass

    @abstractmethod
    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        '''월터의 자기 소개 레포지토리 추상 메소드'''
        pass
