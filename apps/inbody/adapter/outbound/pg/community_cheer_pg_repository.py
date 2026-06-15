from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.adapter.outbound.orm.community_orm import CommunityPostCheer
from inbody.app.dtos.community_dto import CheerDto
from inbody.app.ports.output.community_cheer_repository import CommunityCheerRepository


class CommunityCheerPgRepository(CommunityCheerRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def toggle(self, post_id: int, user_pk: int) -> CheerDto:
        stmt = select(CommunityPostCheer).where(
            CommunityPostCheer.post_id == post_id,
            CommunityPostCheer.user_id == user_pk,
        )
        result = await self._session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            await self._session.delete(existing)
            cheered = False
        else:
            self._session.add(
                CommunityPostCheer(
                    post_id=post_id,
                    user_id=user_pk,
                    created_at=datetime.now(timezone.utc),
                )
            )
            cheered = True
        await self._session.commit()

        count_stmt = (
            select(func.count())
            .select_from(CommunityPostCheer)
            .where(CommunityPostCheer.post_id == post_id)
        )
        cheer_count = (await self._session.execute(count_stmt)).scalar_one()
        return CheerDto(cheer_count=cheer_count, cheered_by_me=cheered)
