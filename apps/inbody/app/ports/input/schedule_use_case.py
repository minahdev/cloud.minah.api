from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.schedule_dto import LessonDeleteCommand, LessonDto, LessonListQuery, LessonSaveCommand


class ScheduleUseCase(ABC):

    @abstractmethod
    async def list_lessons(self, query: LessonListQuery) -> list[LessonDto]:
        pass

    @abstractmethod
    async def save_lesson(self, command: LessonSaveCommand) -> LessonDto:
        pass

    @abstractmethod
    async def delete_lesson(self, command: LessonDeleteCommand) -> None:
        pass
