import bcrypt

from users.adapter.inbound.api.schemas.user_schema import LoginSchema
from users.app.dtos.login_dto import LoginQuery, LoginResult
from users.app.ports.input.login_use_case import LoginUseCase
from users.app.ports.output.login_repository import LoginRepository


class LoginInteractor(LoginUseCase):

    def __init__(self, repository: LoginRepository) -> None:
        self._repository = repository

    async def login_user(self, schema: LoginSchema) -> LoginResult:
        user = await self._repository.find_user(LoginQuery(user_id=schema.userId))
        if user is None:
            raise ValueError("아이디 또는 비밀번호가 올바르지 않습니다.")
        if not bcrypt.checkpw(
            schema.password.encode("utf-8"),
            user.password_hash.encode("utf-8"),
        ):
            raise ValueError("아이디 또는 비밀번호가 올바르지 않습니다.")
        return LoginResult(user_id=user.user_id, role=user.role)
