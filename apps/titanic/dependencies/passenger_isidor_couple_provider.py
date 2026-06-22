"""
IsidorCouple 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(IsidorCouplePgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(IsidorCoupleUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from titanic.adapter.outbound.repositories.passenger_isidor_couple_repository import IsidorCoupleRepository
from titanic.app.ports.output.passenger_isidor_couple_port import IsidorCouplePort
from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.app.use_cases.passenger_isidor_couple_interactor import IsidorCoupleInteractor


def get_isidor_couple_repository(
    db: AsyncSession = Depends(get_db),
) -> IsidorCouplePort:
    return IsidorCoupleRepository(session=db)

def get_passenger_isidor_couple_use_case(
    repository: IsidorCouplePort = Depends(get_isidor_couple_repository),
) -> IsidorCoupleUseCase:
    return IsidorCoupleInteractor(repository=repository)
