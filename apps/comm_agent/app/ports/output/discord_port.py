from abc import ABC, abstractmethod

from comm_agent.app.dtos.discord_dto import DiscordQuery, DiscordResponse

class DiscordPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: DiscordQuery)-> DiscordResponse:
        pass