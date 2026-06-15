from abc import ABC, abstractmethod

from users.adapter.inbound.api.schemas.user_schema import LoginSchema
from users.app.dtos.login_dto import LoginResult


class LoginUseCase(ABC):

    @abstractmethod
    async def login_user(self, schema: LoginSchema) -> LoginResult:
        pass
