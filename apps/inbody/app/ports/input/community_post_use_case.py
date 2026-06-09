from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.community_dto import PostCreateCommand, PostDto


class CommunityPostUseCase(ABC):

    @abstractmethod
    async def list_posts(self, viewer_user_id: str | None) -> list[PostDto]:
        pass

    @abstractmethod
    async def create_post(self, command: PostCreateCommand) -> PostDto:
        pass
