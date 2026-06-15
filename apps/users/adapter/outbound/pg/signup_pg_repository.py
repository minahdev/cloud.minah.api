from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.app.dtos.signup_dto import SignupCommand
from users.app.dtos.user_dto import User
from users.app.ports.output.signup_repository import SignupRepository


class SignupPgRepository(SignupRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_user(self, command: SignupCommand) -> None:
        row = User(
            user_id=command.user_id,
            password_hash=command.password_hash,
            email=command.email,
            nickname=command.nickname,
            role=command.role,
        )
        self._session.add(row)
        await self._session.commit()

    async def find_by_user_id(self, user_id: str) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
