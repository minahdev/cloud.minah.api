"""
RoseModel 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(RoseModelPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(RoseModelUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from titanic.adapter.outbound.pg.passenger_rose_model_pg_repository import RoseModelPgRepository
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db


def get_passenger_rose_model_use_case(
    db: AsyncSession = Depends(get_db),
) -> RoseModelUseCase:
    repository: RoseModelRepository = RoseModelPgRepository(session=db)
    return RoseModelInteractor(repository=repository)
