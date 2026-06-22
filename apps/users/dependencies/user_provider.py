"""
User 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(UserPgRepository, UserService)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(UserUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from users.adapter.outbound.pg.user_pg_repository import UserPgRepository
from users.app.ports.input.user_use_case import UserUseCase
from users.app.ports.output.user_repository import UserRepository
from users.app.use_cases.user_interactor import UserService


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserPgRepository(session=db)


def get_user_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> UserUseCase:
    return UserService(repository=repository)
