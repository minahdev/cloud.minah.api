import logging

from users.app.ports.input.user_use_case import UserUseCase
from users.app.ports.output.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService(UserUseCase):

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def get_user_role(self, user_id: str) -> str:
        user = await self._repository.find_by_user_id(user_id)
        return user.role if user is not None else "user"
