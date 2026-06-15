from abc import ABC, abstractmethod

from users.app.dtos.signup_dto import SignupCommand
from users.app.dtos.user_dto import User


class SignupRepository(ABC):

    @abstractmethod
    async def save_user(self, command: SignupCommand) -> None:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> User | None:
        pass
