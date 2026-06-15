from __future__ import annotations

from abc import ABC, abstractmethod

from users.adapter.inbound.api.schemas.user_schema import UserSchema
from users.app.dtos.user_dto import User


class UserRepository(ABC):

    @abstractmethod
    async def save_user(self, user_schema: UserSchema, password_hash: str) -> None: ...

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> User | None: ...

    @abstractmethod
    async def list_by_role(self, role: str) -> list[User]: ...
