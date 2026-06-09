from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from inbody.app.dtos.train_log_dto import TrainLogDto


class TrainLogRepository(ABC):

    @abstractmethod
    async def list_for_user(self, user_pk: int) -> list[TrainLogDto]:
        pass

    @abstractmethod
    async def get(self, user_pk: int, log_date: date) -> TrainLogDto | None:
        pass

    @abstractmethod
    async def upsert(
        self,
        user_pk: int,
        log_date: date,
        muscles: list[str],
        workout: str,
        weight_kg: float | None,
        diet: dict,
        memo: str,
        exercise_minutes: int | None,
    ) -> TrainLogDto:
        pass
