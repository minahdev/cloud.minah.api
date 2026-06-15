from __future__ import annotations

from abc import ABC, abstractmethod

from users.adapter.inbound.api.schemas.mypage_schema import MyPageProfileResponse, MyPageProfileSchema


class MyPageUseCase(ABC):

    @abstractmethod
    async def get_profile(self, user_id: str) -> MyPageProfileResponse | None: ...

    @abstractmethod
    async def save_profile(self, profile: MyPageProfileSchema) -> None: ...
