"""
WalterRoaster 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(WalterRoasterPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(WalterRoasterUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from titanic.adapter.outbound.repositories.crew_walter_roaster_repository import WalterRoasterRepository
from titanic.app.ports.output.crew_walter_roaster_port import WalterRoasterPort
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.use_cases.crew_walter_roaster_interactor import WalterRoasterInteractor


def get_walter_roaster_repository(
    db: AsyncSession = Depends(get_db),
) -> WalterRoasterPort:
    return WalterRoasterRepository(session=db)

def get_crew_walter_roaster_use_case(
    repository: WalterRoasterPort = Depends(get_walter_roaster_repository),
) -> WalterRoasterUseCase:
    return WalterRoasterInteractor(repository=repository)
