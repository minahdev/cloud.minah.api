"""
ScheduleAccess 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(ScheduleAccessUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from users.adapter.outbound.pg.schedule_pg_access_repository import ScheduleAccessPgRepository
from users.adapter.outbound.pg.user_pg_repository import UserPgRepository
from users.app.ports.input.schedule_access_use_case import ScheduleAccessUseCase
from users.app.ports.output.schedule_access_repository import ScheduleAccessRepository
from users.app.ports.output.user_repository import UserRepository
from users.app.use_cases.schedule_access_interactor import ScheduleAccessService


def get_schedule_access_repository(
    db: AsyncSession = Depends(get_db),
) -> ScheduleAccessRepository:
    return ScheduleAccessPgRepository(session=db)


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserPgRepository(session=db)


def get_schedule_access_use_case(
    repository: ScheduleAccessRepository = Depends(get_schedule_access_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> ScheduleAccessUseCase:
    return ScheduleAccessService(repository=repository, user_repository=user_repository)
