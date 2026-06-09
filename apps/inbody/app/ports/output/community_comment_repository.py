from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.community_dto import CommentDto


class CommunityCommentRepository(ABC):

    @abstractmethod
    async def list_for_post(self, post_id: int) -> list[CommentDto]:
        pass

    @abstractmethod
    async def create(self, post_id: int, author_user_pk: int, author_login_id: str, content: str) -> CommentDto:
        pass
