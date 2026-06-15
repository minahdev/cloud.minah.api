import bcrypt

from users.adapter.inbound.api.schemas.user_schema import UserSchema
from users.app.dtos.signup_dto import SignupCommand, SignupResult
from users.app.ports.input.signup_use_case import SignupUseCase
from users.app.ports.output.signup_repository import SignupRepository


class SignupInteractor(SignupUseCase):

    def __init__(self, repository: SignupRepository) -> None:
        self._repository = repository

    async def save_user(self, schema: UserSchema) -> SignupResult:
        password_hash = bcrypt.hashpw(
            schema.password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")
        command = SignupCommand(
            user_id=schema.userId,
            password_hash=password_hash,
            email=schema.email,
            nickname=schema.nickname,
            role=schema.role,
        )
        await self._repository.save_user(command)
        return SignupResult(user_id=schema.userId)

    async def is_user_id_available(self, user_id: str) -> bool:
        user = await self._repository.find_by_user_id(user_id)
        return user is None
