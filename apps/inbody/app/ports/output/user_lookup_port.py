from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.user_dto import InbodyUserDto


class UserLookupPort(ABC):

    @abstractmethod
    async def require_by_login_id(self, login_id: str) -> InbodyUserDto:
        pass
