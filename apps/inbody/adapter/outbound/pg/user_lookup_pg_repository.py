from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from inbody.app.dtos.user_dto import InbodyUserDto
from inbody.app.ports.output.user_lookup_port import UserLookupPort
from users.adapter.outbound.pg.user_pg_repository import UserPgRepository


class UserLookupPgAdapter(UserLookupPort):

    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserPgRepository(session)

    async def require_by_login_id(self, login_id: str) -> InbodyUserDto:
        user = await self._repo.find_by_user_id(login_id.strip())
        if user is None:
            raise ValueError("사용자를 찾을 수 없습니다.")
        return InbodyUserDto(id=user.id, user_id=user.user_id, role=user.role or "")
