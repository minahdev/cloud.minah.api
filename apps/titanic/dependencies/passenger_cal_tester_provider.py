"""
CalTester 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(CalTesterPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(CalTesterUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from titanic.adapter.outbound.pg.passenger_cal_tester_pg_repository import CalTesterPgRepository
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.use_cases.passenger_cal_tester_interactor import CalTesterInteractor

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db


def get_passenger_cal_tester_use_case(
    db: AsyncSession = Depends(get_db),
) -> CalTesterUseCase:
    repository: CalTesterRepository = CalTesterPgRepository(session=db)
    return CalTesterInteractor(repository=repository)
