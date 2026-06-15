from abc import ABC, abstractmethod

from users.adapter.inbound.api.schemas.user_schema import UserSchema
from users.app.dtos.signup_dto import SignupResult


class SignupUseCase(ABC):

    @abstractmethod
    async def save_user(self, schema: UserSchema) -> SignupResult:
        pass

    @abstractmethod
    async def is_user_id_available(self, user_id: str) -> bool:
        pass
