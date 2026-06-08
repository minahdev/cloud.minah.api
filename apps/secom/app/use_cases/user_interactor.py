import logging

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from secom.adapter.inbound.api.schemas.mypage_schema import (
    MyPageProfileResponse,
    MyPageProfileSchema,
)
from secom.adapter.inbound.api.schemas.user_schema import LoginSchema, UserSchema
from secom.adapter.outbound.pg.user_pg_information_repository import (
    UserInformationRepository,
)
from secom.adapter.outbound.pg.user_pg_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repository = UserRepository(session)
        self.profile_repository = UserInformationRepository(session)

    async def save_user(self, user_schema: UserSchema) -> None:
        logger.info("[UserService] save_user 진입 | userId=%s", user_schema.userId)

        password_hash = bcrypt.hashpw(
            user_schema.password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

        await self.user_repository.save_user(user_schema, password_hash)

        logger.info("[UserService] save_user 완료 | userId=%s", user_schema.userId)

    async def is_user_id_available(self, user_id: str) -> bool:
        logger.info("[UserService] is_user_id_available | userId=%s", user_id)
        user = await self.user_repository.find_by_user_id(user_id)
        return user is None

    async def login_user(self, login_schema: LoginSchema) -> None:
        logger.info("[UserService] login_user 진입 | userId=%s", login_schema.userId)

        user = await self.user_repository.find_by_user_id(login_schema.userId)
        if user is None:
            raise ValueError("아이디 또는 비밀번호가 올바르지 않습니다.")

        if not bcrypt.checkpw(
            login_schema.password.encode("utf-8"),
            user.password_hash.encode("utf-8"),
        ):
            raise ValueError("아이디 또는 비밀번호가 올바르지 않습니다.")

        logger.info("[UserService] login_user 완료 | userId=%s", login_schema.userId)

    async def get_user_role(self, user_id: str) -> str:
        user = await self.user_repository.find_by_user_id(user_id)
        return user.role if user is not None else "user"

    async def get_profile(self, user_id: str) -> MyPageProfileResponse | None:
        logger.info("[UserService] get_profile 진입 | userId=%s", user_id)
        user = await self.user_repository.find_by_user_id(user_id)
        if user is None:
            return None
        profile = await self.profile_repository.get_profile(user_id)
        if profile is not None:
            return profile
        return MyPageProfileResponse(userId=user_id)

    async def save_profile(self, profile: MyPageProfileSchema) -> None:
        logger.info("[UserService] save_profile 진입 | userId=%s", profile.userId)
        await self.profile_repository.save_profile(profile)
        logger.info("[UserService] save_profile 완료 | userId=%s", profile.userId)
