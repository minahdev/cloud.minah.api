from __future__ import annotations

import logging

from inbody.app.dtos.community_dto import CheerCommand, CheerDto
from inbody.app.ports.input.community_cheer_use_case import CommunityCheerUseCase
from inbody.app.ports.output.community_cheer_repository import CommunityCheerRepository
from inbody.app.ports.output.user_lookup_port import UserLookupPort

logger = logging.getLogger(__name__)


class CommunityCheerInteractor(CommunityCheerUseCase):

    def __init__(
        self,
        repository: CommunityCheerRepository,
        user_lookup: UserLookupPort,
    ) -> None:
        self._repo = repository
        self._users = user_lookup

    async def toggle_cheer(self, command: CheerCommand) -> CheerDto:
        user = await self._users.require_by_login_id(command.user_id)
        return await self._repo.toggle(command.post_id, user.id)
