from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.community_dto import PostCreateCommand, PostDto


class CommunityPostRepository(ABC):

    @abstractmethod
    async def list_all(self) -> list[PostDto]:
        pass

    @abstractmethod
    async def get(self, post_id: int) -> PostDto | None:
        pass

    @abstractmethod
    async def create(self, command: PostCreateCommand, author_user_pk: int, author_login_id: str) -> PostDto:
        pass
