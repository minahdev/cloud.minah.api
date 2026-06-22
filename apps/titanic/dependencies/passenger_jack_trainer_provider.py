"""
JackTrainer 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(JackTrainerPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(JackTrainerUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from titanic.adapter.outbound.repositories.passenger_jack_trainer_repository import JackTrainerRepository
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor


def get_jack_trainer_repository(
    db: AsyncSession = Depends(get_db),
) -> JackTrainerPort:
    return JackTrainerRepository(session=db)

def get_jack_trainer(
    repository: JackTrainerPort = Depends(get_jack_trainer_repository),
) -> JackTrainerUseCase:
    return JackTrainerInteractor(repository=repository)
