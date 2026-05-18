import logging

from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


def _format_user(user_schema: UserSchema) -> str:
    return (
        f"userId={user_schema.userId} | password={user_schema.password} | "
        f"email={user_schema.email} | nickname={user_schema.nickname} | role={user_schema.role}"
    )


class UserService:
    def save_user(self, user_schema: UserSchema) -> UserSchema:
        logger.info("[UserService] save_user 진입 | %s", _format_user(user_schema))

        user_repository = UserRepository()
        result = user_repository.save_user(user_schema)

        logger.info("[UserService] save_user 완료 | UserRepository에서 반환")
        return result
