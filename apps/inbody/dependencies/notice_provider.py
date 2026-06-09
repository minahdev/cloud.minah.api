from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from inbody.adapter.outbound.pg.notice_pg_repository import NoticePgRepository
from inbody.adapter.outbound.pg.user_lookup_pg_repository import UserLookupPgAdapter
from inbody.app.ports.input.notice_use_case import NoticeUseCase
from inbody.app.use_cases.notice_interactor import NoticeInteractor


def get_notice_use_case(
    db: AsyncSession = Depends(get_db),
) -> NoticeUseCase:
    return NoticeInteractor(
        repository=NoticePgRepository(db),
        user_lookup=UserLookupPgAdapter(db),
    )
