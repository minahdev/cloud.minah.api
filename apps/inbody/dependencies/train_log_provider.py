from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from inbody.adapter.outbound.pg.train_log_pg_repository import TrainLogPgRepository
from inbody.adapter.outbound.pg.user_lookup_pg_repository import UserLookupPgAdapter
from inbody.app.ports.input.train_log_use_case import TrainLogUseCase
from inbody.app.use_cases.train_log_interactor import TrainLogInteractor


def get_train_log_use_case(
    db: AsyncSession = Depends(get_db),
) -> TrainLogUseCase:
    return TrainLogInteractor(
        repository=TrainLogPgRepository(db),
        user_lookup=UserLookupPgAdapter(db),
    )
