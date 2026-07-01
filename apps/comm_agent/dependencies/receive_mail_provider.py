"""수신 메일 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(ReceivedMailRepository)를 직접 알지 못한다.
- 세션은 core 의 get_db 에서 주입받는다.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from comm_agent.adapter.outbound.repositories.received_mail_repository import ReceivedMailRepository
from comm_agent.app.ports.input.receive_mail_use_case import ReceiveMailUseCase
from comm_agent.app.ports.output.received_mail_port import ReceivedMailRepositoryPort
from comm_agent.app.use_cases.receive_mail_interactor import ReceiveMailInteractor


def get_received_mail_repository(db: AsyncSession = Depends(get_db)) -> ReceivedMailRepositoryPort:
    return ReceivedMailRepository(session=db)


def get_receive_mail_use_case(
    repository: ReceivedMailRepositoryPort = Depends(get_received_mail_repository),
) -> ReceiveMailUseCase:
    return ReceiveMailInteractor(repository=repository)
