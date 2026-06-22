"""
CalTester 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(CalTesterPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(CalTesterUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from titanic.adapter.outbound.repositories.passenger_cal_tester_repository import CalTesterRepository
from titanic.app.ports.output.passenger_cal_tester_port import CalTesterPort
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.use_cases.passenger_cal_tester_interactor import CalTesterInteractor


def get_cal_tester_repository(
    db: AsyncSession = Depends(get_db),
) -> CalTesterPort:
    return CalTesterRepository(session=db)

def get_passenger_cal_tester_use_case(
    repository: CalTesterPort = Depends(get_cal_tester_repository),
) -> CalTesterUseCase:
    return CalTesterInteractor(repository=repository)
