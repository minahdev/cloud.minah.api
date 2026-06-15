from __future__ import annotations

import logging
from datetime import datetime, timezone

from inbody.app.dtos.schedule_dto import LessonDeleteCommand, LessonDto, LessonListQuery, LessonSaveCommand
from inbody.app.ports.input.schedule_use_case import ScheduleUseCase
from inbody.app.ports.output.schedule_repository import ScheduleRepository
from inbody.app.ports.output.user_lookup_port import UserLookupPort
from inbody.app.dtos.user_dto import InbodyUserDto
from users.app.use_cases.schedule_access_interactor import ScheduleAccessService

logger = logging.getLogger(__name__)


class ScheduleInteractor(ScheduleUseCase):

    def __init__(
        self,
        repository: ScheduleRepository,
        user_lookup: UserLookupPort,
        schedule_access: ScheduleAccessService,
    ) -> None:
        self._repo = repository
        self._users = user_lookup
        self._access = schedule_access

    async def _resolve_member(self, actor: InbodyUserDto, member_user_id: str | None) -> InbodyUserDto:
        target_login = (member_user_id or actor.user_id).strip()
        member = await self._users.require_by_login_id(target_login)
        if actor.role not in ("coach", "admin") and member.id != actor.id:
            raise ValueError("다른 회원의 스케줄을 수정할 수 없습니다.")
        return member

    async def list_lessons(self, query: LessonListQuery) -> list[LessonDto]:
        await self._access.require_member_admitted(query.user_id)
        actor = await self._users.require_by_login_id(query.user_id)
        member = await self._resolve_member(actor, query.member_user_id)
        return await self._repo.list_for_member(member.id)

    async def save_lesson(self, command: LessonSaveCommand) -> LessonDto:
        await self._access.require_member_admitted(command.user_id)
        actor = await self._users.require_by_login_id(command.user_id)
        member = await self._resolve_member(actor, command.member_user_id)
        created = None
        if command.created_at:
            try:
                created = datetime.fromisoformat(command.created_at.replace("Z", "+00:00"))
            except ValueError:
                created = datetime.now(timezone.utc)
        return await self._repo.upsert(
            member.id,
            command.client_id,
            command.date,
            command.title,
            command.time,
            command.schedule_note,
            command.record,
            created,
        )

    async def delete_lesson(self, command: LessonDeleteCommand) -> None:
        await self._access.require_member_admitted(command.user_id)
        actor = await self._users.require_by_login_id(command.user_id)
        member = await self._resolve_member(actor, command.member_user_id)
        ok = await self._repo.delete(member.id, command.client_id)
        if not ok:
            raise ValueError("레슨을 찾을 수 없습니다.")
