"""
SmithCaptain 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(SmithCaptainPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(SmithCaptainUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db

from titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import SmithCaptainPgRepository
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.use_cases.crew_smith_captain_interactor import SmithCaptainInteractor


def get_smith_captain_repository(
    db: AsyncSession = Depends(get_db),
) -> SmithCaptainRepository:
    return SmithCaptainPgRepository(session=db)

def get_crew_smith_captain_use_case(
    repository: SmithCaptainRepository = Depends(get_smith_captain_repository),
) -> SmithCaptainUseCase:
    return SmithCaptainInteractor(repository=repository)
