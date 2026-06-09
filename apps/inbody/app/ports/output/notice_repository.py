from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.notice_dto import NoticeDto


class NoticeRepository(ABC):

    @abstractmethod
    async def list_all(self) -> list[NoticeDto]:
        pass

    @abstractmethod
    async def create(self, author_user_pk: int, title: str, body: str) -> NoticeDto:
        pass

    @abstractmethod
    async def delete(self, notice_pk: int) -> bool:
        pass
