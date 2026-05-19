import logging

from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.schemas.mypage_schema import MyPageProfileResponse, MyPageProfileSchema
from secom.app.schemas.user_schema import LoginSchema, UserSchema
from secom.app.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserController:
    def __init__(self, session: AsyncSession) -> None:
        self.user_service = UserService(session)

    async def save_user(self, user_schema: UserSchema) -> None:
        logger.info("[UserController] save_user 진입 | userId=%s", user_schema.userId)

        await self.user_service.save_user(user_schema)

        logger.info("[UserController] save_user 완료 | userId=%s", user_schema.userId)

    async def login_user(self, login_schema: LoginSchema) -> None:
        logger.info("[UserController] login_user 진입 | userId=%s", login_schema.userId)

        await self.user_service.login_user(login_schema)

        logger.info("[UserController] login_user 완료 | userId=%s", login_schema.userId)

    async def get_profile(self, user_id: str) -> MyPageProfileResponse | None:
        logger.info("[UserController] get_profile 진입 | userId=%s", user_id)
        return await self.user_service.get_profile(user_id)

    async def save_profile(self, profile: MyPageProfileSchema) -> None:
        logger.info("[UserController] save_profile 진입 | userId=%s", profile.userId)
        await self.user_service.save_profile(profile)
        logger.info("[UserController] save_profile 완료 | userId=%s", profile.userId)
