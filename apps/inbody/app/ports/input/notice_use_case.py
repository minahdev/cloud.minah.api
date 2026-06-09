from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.notice_dto import NoticeCreateCommand, NoticeDeleteCommand, NoticeDto


class NoticeUseCase(ABC):

    @abstractmethod
    async def list_notices(self) -> list[NoticeDto]:
        pass

    @abstractmethod
    async def create_notice(self, command: NoticeCreateCommand) -> NoticeDto:
        pass

    @abstractmethod
    async def delete_notice(self, command: NoticeDeleteCommand) -> None:
        pass
