from __future__ import annotations

import logging

from inbody.app.dtos.today_story_dto import TodayStorySaveCommand, TodayStoryDto
from inbody.app.ports.input.today_story_use_case import TodayStoryUseCase
from inbody.app.ports.output.today_story_repository import TodayStoryRepository
from inbody.app.ports.output.user_lookup_port import UserLookupPort
from inbody.dates import parse_date_key

logger = logging.getLogger(__name__)


class TodayStoryInteractor(TodayStoryUseCase):

    def __init__(self, repository: TodayStoryRepository, user_lookup: UserLookupPort) -> None:
        self._repo = repository
        self._users = user_lookup

    async def list_stories(self, user_id: str) -> list[TodayStoryDto]:
        user = await self._users.require_by_login_id(user_id)
        return await self._repo.list_for_user(user.id)

    async def get(self, user_id: str, date: str | None) -> TodayStoryDto | None:
        user = await self._users.require_by_login_id(user_id)
        return await self._repo.get(user.id, parse_date_key(date))

    async def save(self, command: TodayStorySaveCommand) -> TodayStoryDto:
        user = await self._users.require_by_login_id(command.user_id)
        return await self._repo.upsert(
            user.id,
            parse_date_key(command.date),
            command.mood,
            command.story.strip(),
        )
