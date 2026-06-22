"""
JamesDirector 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(JamesDirectorPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(JamesDirectorUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from titanic.adapter.outbound.repositories.crew_james_director_repository import JamesDirectorRepository
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.crew_james_director_port import JamesDirectorPort
from titanic.app.use_cases.crew_james_director_interactor import JamesDirectorInteractor


def get_james_director_repository(
    db: AsyncSession = Depends(get_db),
) -> JamesDirectorPort:
    return JamesDirectorRepository(session=db)

def get_crew_james_director_use_case(
    repository: JamesDirectorPort = Depends(get_james_director_repository),
) -> JamesDirectorUseCase:
    return JamesDirectorInteractor(repository=repository)
