from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.app.dtos.login_dto import LoginQuery
from users.app.dtos.user_dto import User
from users.app.ports.output.login_repository import LoginRepository


class LoginPgRepository(LoginRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_user(self, query: LoginQuery) -> User | None:
        stmt = select(User).where(User.user_id == query.user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
