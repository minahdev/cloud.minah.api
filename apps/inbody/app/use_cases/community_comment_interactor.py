from __future__ import annotations

import logging

from inbody.app.dtos.community_dto import CommentCreateCommand, CommentDto
from inbody.app.ports.input.community_comment_use_case import CommunityCommentUseCase
from inbody.app.ports.output.community_comment_repository import CommunityCommentRepository
from inbody.app.ports.output.user_lookup_port import UserLookupPort

logger = logging.getLogger(__name__)


class CommunityCommentInteractor(CommunityCommentUseCase):

    def __init__(
        self,
        repository: CommunityCommentRepository,
        user_lookup: UserLookupPort,
    ) -> None:
        self._repo = repository
        self._users = user_lookup

    async def list_comments(self, post_id: int) -> list[CommentDto]:
        return await self._repo.list_for_post(post_id)

    async def create_comment(self, command: CommentCreateCommand) -> CommentDto:
        user = await self._users.require_by_login_id(command.user_id)
        return await self._repo.create(command.post_id, user.id, user.user_id, command.content.strip())
