"""
LoweBoat 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(LoweBoatPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(LoweBoatUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from titanic.adapter.outbound.repositories.crew_lowe_boat_repository import LoweBoatRepository
from titanic.app.ports.output.crew_lowe_boat_port import LoweBoatPort
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.use_cases.crew_lowe_boat_interactor import LoweBoatInteractor


def get_lowe_boat_repository(
    db: AsyncSession = Depends(get_db),
) -> LoweBoatPort:
    return LoweBoatRepository(session=db)

def get_crew_lowe_boat_use_case(
    repository: LoweBoatPort = Depends(get_lowe_boat_repository),
) -> LoweBoatUseCase:
    return LoweBoatInteractor(repository=repository)
