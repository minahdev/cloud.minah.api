import logging

from secom.app.models.user_model import UserModel
from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


def _format_user(user_schema: UserSchema) -> str:
    return (
        f"userId={user_schema.userId} | password={user_schema.password} | "
        f"email={user_schema.email} | nickname={user_schema.nickname} | role={user_schema.role}"
    )


class UserRepository:
    def save_user(self, user_schema: UserSchema) -> UserSchema:
        logger.info("[UserRepository] save_user 진입 | %s", _format_user(user_schema))

        # TODO: UserModel로 DB 저장
        _user_model = UserModel()

        logger.info("[UserRepository] save_user 완료 | UserModel 처리 후 반환")
        return user_schema
