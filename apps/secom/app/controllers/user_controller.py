import logging

from secom.app.schemas.user_schema import UserSchema
from secom.app.services.user_service import UserService

logger = logging.getLogger(__name__)


def _format_user(user_schema: UserSchema) -> str:
    return (
        f"userId={user_schema.userId} | password={user_schema.password} | "
        f"email={user_schema.email} | nickname={user_schema.nickname} | role={user_schema.role}"
    )


class UserController:
    def save_user(self, user_schema: UserSchema) -> UserSchema:
        logger.info("[UserController] save_user 진입 | %s", _format_user(user_schema))

        user_service = UserService()
        result = user_service.save_user(user_schema)

        logger.info("[UserController] save_user 완료 | UserService에서 반환")
        return result
