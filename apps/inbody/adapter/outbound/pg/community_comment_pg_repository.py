from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.adapter.outbound.orm.community_orm import CommunityComment
from inbody.app.dtos.community_dto import CommentDto
from inbody.app.ports.output.community_comment_repository import CommunityCommentRepository


def _to_dto(row: CommunityComment) -> CommentDto:
    return CommentDto(
        id=str(row.id),
        author_id=str(row.author_user_id),
        content=row.content or "",
        created_at=row.created_at.isoformat() if row.created_at else "",
    )


class CommunityCommentPgRepository(CommunityCommentRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_post(self, post_id: int) -> list[CommentDto]:
        stmt = (
            select(CommunityComment)
            .where(CommunityComment.post_id == post_id)
            .order_by(CommunityComment.created_at.asc())
        )
        result = await self._session.execute(stmt)
        return [_to_dto(r) for r in result.scalars().all()]

    async def create(
        self,
        post_id: int,
        author_user_pk: int,
        author_login_id: str,
        content: str,
    ) -> CommentDto:
        row = CommunityComment(
            post_id=post_id,
            author_user_id=author_user_pk,
            content=content,
            created_at=datetime.now(timezone.utc),
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _to_dto(row)
