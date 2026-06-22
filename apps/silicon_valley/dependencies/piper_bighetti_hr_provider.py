from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from silicon_valley.adapter.outbound.repositories.piper_bighetti_hr_repository import BighettiHrRepository
from silicon_valley.app.ports.output.piper_bighetti_hr_port import BighettiHrPort
from silicon_valley.app.ports.input.piper_bighetti_hr_use_case import BighettiHrUseCase
from silicon_valley.app.use_cases.piper_bighetti_hr_interactor import BighettiHrInteractor


def get_bighetti_hr_repository(db: AsyncSession = Depends(get_db)) -> BighettiHrPort:
    return BighettiHrRepository(session=db)


def get_piper_bighetti_hr_use_case(
    repository: BighettiHrPort = Depends(get_bighetti_hr_repository),
) -> BighettiHrUseCase:
    return BighettiHrInteractor(repository=repository)
