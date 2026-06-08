"""
WalterRoaster 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(WalterRoasterPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(WalterRoasterUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import WalterRoasterPgRepository
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.use_cases.crew_walter_roaster_interactor import WalterRoasterInteractor

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db

#WalterRoasterUseCase : 타입
def get_crew_walter_roaster_use_case(
    db : AsyncSession = Depends(get_db)
) -> WalterRoasterUseCase:
    repository : WalterRoasterRepository = WalterRoasterPgRepository(session=db)
    return WalterRoasterInteractor(repository=repository)




