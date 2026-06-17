from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse

class AndrewsArchitectPort(ABC):


    @abstractmethod
    def analyze_intent(self, question: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 질문 의도를 파악하는 추상 메소드'''
        pass

    @abstractmethod
    def introduce_myself(self, query: AndrewsArchitectQuery) -> AndrewsArchitectResponse:
        '''앤드류 설계자의 자기 소개 레포지토리 추상 메소드'''
        pass
