from abc import ABC, abstractmethod

from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainQuery, SmithCaptainChatCommand

class SmithCaptainPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: SmithCaptainQuery)->SmithCaptainResponse:
        pass

    @abstractmethod
    async def chat(self, command: SmithCaptainChatCommand) -> SmithCaptainResponse:
        pass