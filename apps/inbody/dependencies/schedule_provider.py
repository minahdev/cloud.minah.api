from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from inbody.adapter.outbound.pg.schedule_pg_repository import SchedulePgRepository
from inbody.adapter.outbound.pg.user_lookup_pg_repository import UserLookupPgAdapter
from inbody.app.ports.input.schedule_use_case import ScheduleUseCase
from inbody.app.use_cases.schedule_interactor import ScheduleInteractor
from users.app.use_cases.schedule_access_interactor import ScheduleAccessService


def get_schedule_use_case(
    db: AsyncSession = Depends(get_db),
) -> ScheduleUseCase:
    return ScheduleInteractor(
        repository=SchedulePgRepository(db),
        user_lookup=UserLookupPgAdapter(db),
        schedule_access=ScheduleAccessService(db),
    )
