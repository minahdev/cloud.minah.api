from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.today_story_dto import TodayStorySaveCommand, TodayStoryDto


class TodayStoryUseCase(ABC):

    @abstractmethod
    async def list_stories(self, user_id: str) -> list[TodayStoryDto]:
        pass

    @abstractmethod
    async def get(self, user_id: str, date: str | None) -> TodayStoryDto | None:
        pass

    @abstractmethod
    async def save(self, command: TodayStorySaveCommand) -> TodayStoryDto:
        pass
