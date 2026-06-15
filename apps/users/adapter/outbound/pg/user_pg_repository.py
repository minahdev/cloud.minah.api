import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.adapter.inbound.api.schemas.user_schema import UserSchema
from users.app.dtos.user_dto import User
from users.app.ports.output.user_repository import UserRepository as UserRepositoryPort

logger = logging.getLogger(__name__)


class UserPgRepository(UserRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_user(self, user_schema: UserSchema, password_hash: str) -> None:
        logger.info(
            "[UserRepository] save_user 진입 | userId=%s | email=%s | nickname=%s | role=%s",
            user_schema.userId,
            user_schema.email,
            user_schema.nickname,
            user_schema.role,
        )

        row = User(
            user_id=user_schema.userId,
            password_hash=password_hash,
            email=user_schema.email,
            nickname=user_schema.nickname,
            role=user_schema.role,
        )
        self._session.add(row)
        await self._session.commit()

        logger.info("[UserRepository] save_user 완료 | Neon INSERT userId=%s", user_schema.userId)

    async def find_by_user_id(self, user_id: str) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_role(self, role: str) -> list[User]:
        stmt = select(User).where(User.role == role).order_by(User.nickname)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
