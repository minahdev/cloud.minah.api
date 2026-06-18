from abc import ABC, abstractmethod
from typing import Any
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema, ChatSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse

class SmithCaptainUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 메소드'''
        pass

    @abstractmethod
    async def chat(self, question: str) -> SmithCaptainResponse:
        '''사용자 자연어 입력을 받아 채팅 응답을 반환'''
        pass

