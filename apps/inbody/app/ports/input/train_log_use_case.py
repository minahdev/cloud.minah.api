from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.train_log_dto import TrainLogSaveCommand, TrainLogDto


class TrainLogUseCase(ABC):

    @abstractmethod
    async def list_logs(self, user_id: str) -> list[TrainLogDto]:
        pass

    @abstractmethod
    async def get(self, user_id: str, date: str) -> TrainLogDto | None:
        pass

    @abstractmethod
    async def save(self, command: TrainLogSaveCommand) -> TrainLogDto:
        pass
