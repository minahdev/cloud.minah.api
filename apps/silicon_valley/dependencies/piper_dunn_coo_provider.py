from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from silicon_valley.adapter.outbound.repositories.piper_dunn_coo_repository import DunnCooRepository
from silicon_valley.app.ports.output.piper_dunn_coo_port import DunnCooPort
from silicon_valley.app.ports.input.piper_dunn_coo_use_case import DunnCooUseCase
from silicon_valley.app.use_cases.piper_dunn_coo_interactor import DunnCooInteractor


def get_dunn_coo_repository(db: AsyncSession = Depends(get_db)) -> DunnCooPort:
    return DunnCooRepository(session=db)


def get_piper_dunn_coo_use_case(
    repository: DunnCooPort = Depends(get_dunn_coo_repository),
) -> DunnCooUseCase:
    return DunnCooInteractor(repository=repository)
