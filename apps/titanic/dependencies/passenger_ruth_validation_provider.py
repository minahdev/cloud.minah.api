"""
RuthValidation 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(RuthValidationPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(RuthValidationUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from titanic.adapter.outbound.repositories.passenger_ruth_validation_repository import RuthValidationRepository
from titanic.app.ports.output.passenger_ruth_validation_port import RuthValidationPort
from titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from titanic.app.use_cases.passenger_ruth_validation_interactor import RuthValidationInteractor


def get_ruth_validation_repository(
    db: AsyncSession = Depends(get_db),
) -> RuthValidationPort:
    return RuthValidationRepository(session=db)

def get_passenger_ruth_survivor_use_case(
    repository: RuthValidationPort = Depends(get_ruth_validation_repository),
) -> RuthValidationUseCase:
    return RuthValidationInteractor(repository=repository)
