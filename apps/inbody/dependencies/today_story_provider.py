from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from inbody.adapter.outbound.pg.today_story_pg_repository import TodayStoryPgRepository
from inbody.adapter.outbound.pg.user_lookup_pg_repository import UserLookupPgAdapter
from inbody.app.ports.input.today_story_use_case import TodayStoryUseCase
from inbody.app.use_cases.today_story_interactor import TodayStoryInteractor


def get_today_story_use_case(
    db: AsyncSession = Depends(get_db),
) -> TodayStoryUseCase:
    return TodayStoryInteractor(
        repository=TodayStoryPgRepository(db),
        user_lookup=UserLookupPgAdapter(db),
    )
