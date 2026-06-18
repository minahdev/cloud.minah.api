from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse

class AndrewsArchitectUseCase(ABC):

    @abstractmethod
    def analyze_intent(self, question: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 프론트 질문의 의도를 파악하는 추상 메소드'''
        pass

    @abstractmethod
    def answer(self, question: str, train_set: pd.DataFrame, champion_strategy: Any = None) -> str:
        '''의도 분석 + 데이터 기반 자연어 답변 생성'''
        pass

    @abstractmethod
    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        pass
