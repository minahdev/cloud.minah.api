from abc import ABC, abstractmethod
from comm_agent.adapter.inbound.api.schemas.discord_schema import DiscordIntroduceSchema
from comm_agent.app.dtos.discord_dto import DiscordResponse

class DiscordUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: DiscordIntroduceSchema)-> DiscordResponse:
        pass
