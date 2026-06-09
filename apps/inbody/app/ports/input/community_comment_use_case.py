from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.community_dto import CommentCreateCommand, CommentDto


class CommunityCommentUseCase(ABC):

    @abstractmethod
    async def list_comments(self, post_id: int) -> list[CommentDto]:
        pass

    @abstractmethod
    async def create_comment(self, command: CommentCreateCommand) -> CommentDto:
        pass
