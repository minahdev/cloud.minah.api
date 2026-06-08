from sqlalchemy.ext.asyncio import AsyncSession

from secom.adapter.outbound.pg.user_pg_repository import UserRepository
from secom.app.dtos.user_model import User


async def require_user(session: AsyncSession, login_user_id: str) -> User:
    user = await UserRepository(session).find_by_user_id(login_user_id.strip())
    if user is None:
        raise ValueError("사용자를 찾을 수 없습니다.")
    return user
