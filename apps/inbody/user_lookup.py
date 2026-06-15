from sqlalchemy.ext.asyncio import AsyncSession

from users.adapter.outbound.pg.user_pg_repository import UserPgRepository as UserRepository
from users.app.dtos.user_dto import User


async def require_user(session: AsyncSession, login_user_id: str) -> User:
    user = await UserRepository(session).find_by_user_id(login_user_id.strip())
    if user is None:
        raise ValueError("사용자를 찾을 수 없습니다.")
    return user
