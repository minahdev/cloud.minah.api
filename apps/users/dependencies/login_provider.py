"""
Login 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(LoginPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(LoginUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from users.adapter.outbound.pg.login_pg_repository import LoginPgRepository
from users.app.ports.input.login_use_case import LoginUseCase
from users.app.ports.output.login_repository import LoginRepository
from users.app.use_cases.login_interactor import LoginInteractor


def get_login_repository(
    db: AsyncSession = Depends(get_db),
) -> LoginRepository:
    return LoginPgRepository(session=db)


def get_login_use_case(
    repository: LoginRepository = Depends(get_login_repository),
) -> LoginUseCase:
    return LoginInteractor(repository=repository)
