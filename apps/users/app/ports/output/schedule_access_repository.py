from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from users.app.dtos.schedule_access_dto import ScheduleAccess
from users.app.dtos.schedule_access_grant_dto import ScheduleAccessGrant
from users.app.dtos.schedule_invite_code_dto import ScheduleInviteCode


class ScheduleAccessRepository(ABC):

    @abstractmethod
    async def get_row(self) -> ScheduleAccess | None: ...

    @abstractmethod
    async def upsert_password(self, password_hash: str, coach_user_id: str) -> ScheduleAccess: ...

    @abstractmethod
    async def clear_grants(self) -> None: ...

    @abstractmethod
    async def grant_user(self, user_id: str) -> None: ...

    @abstractmethod
    async def is_admitted(self, user_id: str) -> bool: ...

    @abstractmethod
    async def list_admitted_members(self) -> list[tuple[str, str]]: ...

    @abstractmethod
    async def create_invite_code(
        self,
        code_digest: str,
        created_by_user_id: str,
        expires_at: datetime,
        *,
        max_uses: int = 1,
    ) -> ScheduleInviteCode: ...

    @abstractmethod
    async def find_redeemable_invite(self, code_digest: str) -> ScheduleInviteCode | None: ...

    @abstractmethod
    async def mark_invite_used(self, invite_id: int) -> None: ...

    @abstractmethod
    async def count_active_invite_codes(self) -> int: ...
