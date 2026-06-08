"""
JackTrainer 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(JackTrainerPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(JackTrainerUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackTrainerPgRepository
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db


def get_passenger_jack_trainer_use_case(
    db: AsyncSession = Depends(get_db),
) -> JackTrainerUseCase:
    repository: JackTrainerRepository = JackTrainerPgRepository(session=db)
    return JackTrainerInteractor(repository=repository)
