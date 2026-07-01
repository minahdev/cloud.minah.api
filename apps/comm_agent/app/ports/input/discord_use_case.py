from __future__ import annotations

from abc import ABC, abstractmethod

from comm_agent.app.dtos.email_send_dto import IntroduceResponse


class DiscordUseCase(ABC):
    """Discord 채널 유스케이스."""

    @abstractmethod
    async def introduce_myself(self, id: int, name: str) -> IntroduceResponse:
        pass
