from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from silicon_valley.adapter.outbound.repositories.piper_gilfoyle_sys_repository import GilfoyleSysRepository
from silicon_valley.app.ports.output.piper_gilfoyle_sys_port import GilfoyleSysPort
from silicon_valley.app.ports.input.piper_gilfoyle_sys_use_case import GilfoyleSysUseCase
from silicon_valley.app.use_cases.piper_gilfoyle_sys_interactor import GilfoyleSysInteractor


def get_gilfoyle_sys_repository(db: AsyncSession = Depends(get_db)) -> GilfoyleSysPort:
    return GilfoyleSysRepository(session=db)


def get_piper_gilfoyle_sys_use_case(
    repository: GilfoyleSysPort = Depends(get_gilfoyle_sys_repository),
) -> GilfoyleSysUseCase:
    return GilfoyleSysInteractor(repository=repository)
