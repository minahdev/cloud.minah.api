"""주소록 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(ContactRepository)를 직접 알지 못한다.
- 세션은 core 의 get_db 에서 주입받는다.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from comm_agent.adapter.outbound.repositories.contact_repository import ContactRepository
from comm_agent.app.ports.input.contact_use_case import ManageContactsUseCase
from comm_agent.app.ports.output.contact_port import ContactRepositoryPort
from comm_agent.app.use_cases.contact_interactor import ManageContactsInteractor


def get_contact_repository(db: AsyncSession = Depends(get_db)) -> ContactRepositoryPort:
    return ContactRepository(session=db)


def get_manage_contacts_use_case(
    repository: ContactRepositoryPort = Depends(get_contact_repository),
) -> ManageContactsUseCase:
    return ManageContactsInteractor(repository=repository)
