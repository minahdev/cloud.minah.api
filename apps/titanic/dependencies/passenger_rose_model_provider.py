"""
RoseModel 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(RoseModelPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(RoseModelUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from titanic.adapter.outbound.repositories.passenger_rose_model_repository import RoseModelRepository
from titanic.app.ports.output.passenger_rose_model_port import RoseModelPort
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor


def get_rose_model_repository(
    db: AsyncSession = Depends(get_db),
) -> RoseModelPort:
    return RoseModelRepository(session=db)

def get_rose_model(
    repository: RoseModelPort = Depends(get_rose_model_repository),
) -> RoseModelUseCase:
    return RoseModelInteractor(repository=repository)
