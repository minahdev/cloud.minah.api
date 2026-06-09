from __future__ import annotations

import logging

from inbody.app.dtos.notice_dto import NoticeCreateCommand, NoticeDeleteCommand, NoticeDto
from inbody.app.ports.input.notice_use_case import NoticeUseCase
from inbody.app.ports.output.notice_repository import NoticeRepository
from inbody.app.ports.output.user_lookup_port import UserLookupPort

logger = logging.getLogger(__name__)


class NoticeInteractor(NoticeUseCase):

    def __init__(self, repository: NoticeRepository, user_lookup: UserLookupPort) -> None:
        self._repo = repository
        self._users = user_lookup

    async def list_notices(self) -> list[NoticeDto]:
        return await self._repo.list_all()

    async def create_notice(self, command: NoticeCreateCommand) -> NoticeDto:
        user = await self._users.require_by_login_id(command.user_id)
        if user.role != "admin":
            raise ValueError("관리자만 공지를 등록할 수 있습니다.")
        return await self._repo.create(user.id, command.title.strip(), command.body.strip())

    async def delete_notice(self, command: NoticeDeleteCommand) -> None:
        user = await self._users.require_by_login_id(command.user_id)
        if user.role != "admin":
            raise ValueError("관리자만 공지를 삭제할 수 있습니다.")
        try:
            pk = int(command.notice_id)
        except ValueError as e:
            raise ValueError("잘못된 공지 ID입니다.") from e
        ok = await self._repo.delete(pk)
        if not ok:
            raise ValueError("공지를 찾을 수 없습니다.")
