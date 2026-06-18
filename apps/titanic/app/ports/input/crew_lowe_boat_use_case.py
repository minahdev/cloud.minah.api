from abc import ABC, abstractmethod

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse

class LoweBoatUseCase(ABC):

    @abstractmethod
    def feature_engineering(self, train_set: pd.DataFrame) -> tuple[list[list[float]], list[int]]:
        '''전처리된 (X_train, y_label) 반환'''
        pass

    @abstractmethod
    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        pass

