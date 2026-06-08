"""
LoweBoat 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(LoweBoatPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(LoweBoatUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from titanic.adapter.outbound.pg.crew_lowe_boat_pg_repository import LoweBoatPgRepository
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.use_cases.crew_lowe_boat_interactor import LoweBoatInteractor

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db


def get_crew_lowe_boat_use_case(
    db: AsyncSession = Depends(get_db),
) -> LoweBoatUseCase:
    repository: LoweBoatRepository = LoweBoatPgRepository(session=db)
    return LoweBoatInteractor(repository=repository)
