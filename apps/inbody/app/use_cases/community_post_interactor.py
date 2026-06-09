from __future__ import annotations

import logging

from inbody.app.dtos.community_dto import PostCreateCommand, PostDto
from inbody.app.ports.input.community_post_use_case import CommunityPostUseCase
from inbody.app.ports.output.community_post_repository import CommunityPostRepository
from inbody.app.ports.output.user_lookup_port import UserLookupPort

logger = logging.getLogger(__name__)


class CommunityPostInteractor(CommunityPostUseCase):

    def __init__(
        self,
        repository: CommunityPostRepository,
        user_lookup: UserLookupPort,
    ) -> None:
        self._repo = repository
        self._users = user_lookup

    async def list_posts(self) -> list[PostDto]:
        return await self._repo.list_all()

    async def create_post(self, command: PostCreateCommand) -> PostDto:
        user = await self._users.require_by_login_id(command.user_id)
        return await self._repo.create(command, user.id, user.user_id)
