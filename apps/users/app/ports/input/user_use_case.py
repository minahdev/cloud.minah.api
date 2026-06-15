from __future__ import annotations

from abc import ABC, abstractmethod


class UserUseCase(ABC):

    @abstractmethod
    async def get_user_role(self, user_id: str) -> str: ...
