from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.community_dto import CheerDto


class CommunityCheerRepository(ABC):

    @abstractmethod
    async def toggle(self, post_id: int, user_pk: int) -> CheerDto:
        pass
