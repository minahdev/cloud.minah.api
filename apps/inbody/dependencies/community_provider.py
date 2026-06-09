from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from inbody.adapter.outbound.pg.community_cheer_pg_repository import CommunityCheerPgRepository
from inbody.adapter.outbound.pg.community_comment_pg_repository import CommunityCommentPgRepository
from inbody.adapter.outbound.pg.community_media_local_adapter import CommunityMediaLocalAdapter
from inbody.adapter.outbound.pg.community_post_pg_repository import CommunityPostPgRepository
from inbody.adapter.outbound.pg.user_lookup_pg_repository import UserLookupPgAdapter
from inbody.app.ports.input.community_cheer_use_case import CommunityCheerUseCase
from inbody.app.ports.input.community_comment_use_case import CommunityCommentUseCase
from inbody.app.ports.input.community_media_use_case import CommunityMediaUseCase
from inbody.app.ports.input.community_post_use_case import CommunityPostUseCase
from inbody.app.use_cases.community_cheer_interactor import CommunityCheerInteractor
from inbody.app.use_cases.community_comment_interactor import CommunityCommentInteractor
from inbody.app.use_cases.community_media_interactor import CommunityMediaInteractor
from inbody.app.use_cases.community_post_interactor import CommunityPostInteractor
from inbody.community_media import get_community_media_storage


def get_community_post_use_case(
    db: AsyncSession = Depends(get_db),
) -> CommunityPostUseCase:
    return CommunityPostInteractor(
        repository=CommunityPostPgRepository(db),
        user_lookup=UserLookupPgAdapter(db),
    )


def get_community_cheer_use_case(
    db: AsyncSession = Depends(get_db),
) -> CommunityCheerUseCase:
    return CommunityCheerInteractor(
        repository=CommunityCheerPgRepository(db),
        user_lookup=UserLookupPgAdapter(db),
    )


def get_community_comment_use_case(
    db: AsyncSession = Depends(get_db),
) -> CommunityCommentUseCase:
    return CommunityCommentInteractor(
        repository=CommunityCommentPgRepository(db),
        user_lookup=UserLookupPgAdapter(db),
    )


def get_community_media_use_case(
    db: AsyncSession = Depends(get_db),
) -> CommunityMediaUseCase:
    return CommunityMediaInteractor(
        media_port=CommunityMediaLocalAdapter(get_community_media_storage()),
        user_lookup=UserLookupPgAdapter(db),
    )
