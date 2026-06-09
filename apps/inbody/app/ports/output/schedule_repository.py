from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from inbody.app.dtos.schedule_dto import LessonDto


class ScheduleRepository(ABC):

    @abstractmethod
    async def list_for_member(self, member_user_pk: int) -> list[LessonDto]:
        pass

    @abstractmethod
    async def upsert(
        self,
        member_user_pk: int,
        client_id: str,
        lesson_date: str,
        title: str,
        time: str,
        schedule_note: str,
        record: dict | None,
        created_at: datetime | None,
    ) -> LessonDto:
        pass

    @abstractmethod
    async def delete(self, member_user_pk: int, client_id: str) -> bool:
        pass
