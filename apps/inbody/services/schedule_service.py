from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from inbody.models.schedule_model import Lesson
from inbody.repositories.schedule_repository import ScheduleRepository
from inbody.schemas.schedule_schema import LessonPayload, LessonResponse
from inbody.user_lookup import require_user
from secom.adapter.outbound.pg.user_pg_repository import UserRepository
from secom.app.use_cases.schedule_access_interactor import ScheduleAccessService


def _to_response(row: Lesson, member_login_id: str) -> LessonResponse:
    return LessonResponse(
        id=row.client_id,
        date=row.lesson_date,
        title=row.title,
        time=row.time,
        scheduleNote=row.schedule_note,
        record=row.record,
        createdAt=row.created_at.isoformat().replace("+00:00", "Z"),
        memberUserId=member_login_id,
    )


class ScheduleService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ScheduleRepository(session)
        self._users = UserRepository(session)
        self._session = session

    async def _resolve_member(self, login_user_id: str, member_user_id: str | None):
        actor = await require_user(self._session, login_user_id)
        target_login = (member_user_id or login_user_id).strip()
        member = await self._users.find_by_user_id(target_login)
        if member is None:
            raise ValueError("회원을 찾을 수 없습니다.")
        if actor.role not in ("coach", "admin") and member.id != actor.id:
            raise ValueError("다른 회원의 스케줄을 수정할 수 없습니다.")
        return member

    async def list_lessons(
        self, login_user_id: str, member_user_id: str | None
    ) -> list[LessonResponse]:
        await ScheduleAccessService(self._session).require_member_admitted(login_user_id)
        member = await self._resolve_member(login_user_id, member_user_id)
        rows = await self._repo.list_for_member(member.id)
        return [_to_response(r, member.user_id) for r in rows]

    async def save_lesson(self, payload: LessonPayload) -> LessonResponse:
        await ScheduleAccessService(self._session).require_member_admitted(payload.userId)
        member = await self._resolve_member(payload.userId, payload.memberUserId)
        created = None
        if payload.createdAt:
            try:
                created = datetime.fromisoformat(payload.createdAt.replace("Z", "+00:00"))
            except ValueError:
                created = datetime.now(timezone.utc)
        row = await self._repo.upsert(
            member.id,
            payload.id,
            payload.date,
            payload.title,
            payload.time,
            payload.scheduleNote,
            payload.record,
            created,
        )
        return _to_response(row, member.user_id)

    async def delete_lesson(
        self, login_user_id: str, member_user_id: str | None, client_id: str
    ) -> None:
        await ScheduleAccessService(self._session).require_member_admitted(login_user_id)
        member = await self._resolve_member(login_user_id, member_user_id)
        ok = await self._repo.delete(member.id, client_id)
        if not ok:
            raise ValueError("레슨을 찾을 수 없습니다.")
