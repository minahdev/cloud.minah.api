from __future__ import annotations

import logging

from inbody.app.dtos.train_log_dto import TrainLogSaveCommand, TrainLogDto
from inbody.app.ports.input.train_log_use_case import TrainLogUseCase
from inbody.app.ports.output.train_log_repository import TrainLogRepository
from inbody.app.ports.output.user_lookup_port import UserLookupPort
from inbody.dates import parse_date_key

logger = logging.getLogger(__name__)


class TrainLogInteractor(TrainLogUseCase):

    def __init__(self, repository: TrainLogRepository, user_lookup: UserLookupPort) -> None:
        self._repo = repository
        self._users = user_lookup

    async def list_logs(self, user_id: str) -> list[TrainLogDto]:
        user = await self._users.require_by_login_id(user_id)
        return await self._repo.list_for_user(user.id)

    async def get(self, user_id: str, date: str) -> TrainLogDto | None:
        user = await self._users.require_by_login_id(user_id)
        return await self._repo.get(user.id, parse_date_key(date))

    async def save(self, command: TrainLogSaveCommand) -> TrainLogDto:
        user = await self._users.require_by_login_id(command.user_id)
        return await self._repo.upsert(
            user.id,
            parse_date_key(command.date),
            command.muscles,
            command.workout,
            command.weight_kg,
            command.diet,
            command.memo,
            command.exercise_minutes,
        )
