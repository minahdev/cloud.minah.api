from __future__ import annotations

from abc import ABC, abstractmethod


class ScheduleAccessUseCase(ABC):

    @abstractmethod
    async def is_configured(self) -> bool: ...

    @abstractmethod
    async def is_admitted(self, user_id: str) -> bool: ...

    @abstractmethod
    async def verify_and_grant(self, user_id: str, password: str) -> None: ...

    @abstractmethod
    async def create_invite_code(self, coach_user_id: str) -> dict[str, str]: ...

    @abstractmethod
    async def redeem_invite_code(self, user_id: str, code: str) -> None: ...

    @abstractmethod
    async def require_member_admitted(self, login_user_id: str) -> None: ...

    @abstractmethod
    async def set_password(self, coach_user_id: str, password: str) -> None: ...

    @abstractmethod
    async def list_admitted_members_for_coach(self, requester_user_id: str) -> list[dict[str, str]]: ...
