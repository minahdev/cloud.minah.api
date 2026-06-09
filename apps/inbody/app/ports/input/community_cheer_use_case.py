from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.community_dto import CheerCommand, CheerDto


class CommunityCheerUseCase(ABC):

    @abstractmethod
    async def toggle_cheer(self, command: CheerCommand) -> CheerDto:
        pass
