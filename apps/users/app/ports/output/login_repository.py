from abc import ABC, abstractmethod

from users.app.dtos.login_dto import LoginQuery
from users.app.dtos.user_dto import User


class LoginRepository(ABC):

    @abstractmethod
    async def find_user(self, query: LoginQuery) -> User | None:
        pass
