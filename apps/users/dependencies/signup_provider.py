"""
Signup 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(SignupPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(SignupUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from users.adapter.outbound.pg.signup_pg_repository import SignupPgRepository
from users.app.ports.input.signup_use_case import SignupUseCase
from users.app.ports.output.signup_repository import SignupRepository
from users.app.use_cases.signup_interactor import SignupInteractor


def get_signup_repository(
    db: AsyncSession = Depends(get_db),
) -> SignupRepository:
    return SignupPgRepository(session=db)


def get_signup_use_case(
    repository: SignupRepository = Depends(get_signup_repository),
) -> SignupUseCase:
    return SignupInteractor(repository=repository)
