from datetime import datetime, timezone

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from users.app.dtos.schedule_access_grant_dto import ScheduleAccessGrant
from users.app.dtos.schedule_access_dto import ScheduleAccess
from users.app.dtos.schedule_invite_code_dto import ScheduleInviteCode
from users.app.dtos.user_dto import User
from users.app.ports.output.schedule_access_repository import ScheduleAccessRepository as ScheduleAccessRepositoryPort


class ScheduleAccessPgRepository(ScheduleAccessRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_row(self) -> ScheduleAccess | None:
        result = await self._session.execute(select(ScheduleAccess).limit(1))
        return result.scalar_one_or_none()

    async def upsert_password(self, password_hash: str, coach_user_id: str) -> ScheduleAccess:
        row = await self.get_row()
        now = datetime.now(timezone.utc)
        if row is None:
            row = ScheduleAccess(
                password_hash=password_hash,
                updated_by_user_id=coach_user_id,
                updated_at=now,
            )
            self._session.add(row)
        else:
            row.password_hash = password_hash
            row.updated_by_user_id = coach_user_id
            row.updated_at = now
        await self._session.commit()
        await self._session.refresh(row)
        return row

    async def clear_grants(self) -> None:
        await self._session.execute(delete(ScheduleAccessGrant))
        await self._session.commit()

    async def grant_user(self, user_id: str) -> None:
        now = datetime.now(timezone.utc)
        result = await self._session.execute(
            select(ScheduleAccessGrant).where(ScheduleAccessGrant.user_id == user_id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            self._session.add(ScheduleAccessGrant(user_id=user_id, granted_at=now))
        else:
            row.granted_at = now
        await self._session.commit()

    async def is_admitted(self, user_id: str) -> bool:
        result = await self._session.execute(
            select(ScheduleAccessGrant.id).where(ScheduleAccessGrant.user_id == user_id).limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def list_admitted_members(self) -> list[tuple[str, str]]:
        stmt = (
            select(User.user_id, User.nickname)
            .join(ScheduleAccessGrant, ScheduleAccessGrant.user_id == User.user_id)
            .where(User.role == "user")
            .order_by(User.nickname)
        )
        result = await self._session.execute(stmt)
        return [(r[0], r[1]) for r in result.all()]

    async def create_invite_code(
        self,
        code_digest: str,
        created_by_user_id: str,
        expires_at: datetime,
        *,
        max_uses: int = 1,
    ) -> ScheduleInviteCode:
        now = datetime.now(timezone.utc)
        row = ScheduleInviteCode(
            code_digest=code_digest,
            created_by_user_id=created_by_user_id,
            expires_at=expires_at,
            max_uses=max_uses,
            use_count=0,
            created_at=now,
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return row

    async def find_redeemable_invite(self, code_digest: str) -> ScheduleInviteCode | None:
        now = datetime.now(timezone.utc)
        stmt = (
            select(ScheduleInviteCode)
            .where(
                ScheduleInviteCode.code_digest == code_digest,
                ScheduleInviteCode.use_count < ScheduleInviteCode.max_uses,
                ScheduleInviteCode.expires_at > now,
            )
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_invite_used(self, invite_id: int) -> None:
        result = await self._session.execute(
            select(ScheduleInviteCode).where(ScheduleInviteCode.id == invite_id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return
        row.use_count += 1
        await self._session.commit()

    async def count_active_invite_codes(self) -> int:
        now = datetime.now(timezone.utc)
        stmt = select(func.count()).select_from(ScheduleInviteCode).where(
            ScheduleInviteCode.use_count < ScheduleInviteCode.max_uses,
            ScheduleInviteCode.expires_at > now,
        )
        result = await self._session.execute(stmt)
        return int(result.scalar_one() or 0)
