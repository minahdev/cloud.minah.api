from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from inbody.app.dtos.today_story_dto import TodayStoryDto


class TodayStoryRepository(ABC):

    @abstractmethod
    async def list_for_user(self, user_pk: int) -> list[TodayStoryDto]:
        pass

    @abstractmethod
    async def get(self, user_pk: int, story_date: date) -> TodayStoryDto | None:
        pass

    @abstractmethod
    async def upsert(
        self,
        user_pk: int,
        story_date: date,
        mood: str | None,
        story: str,
    ) -> TodayStoryDto:
        pass
