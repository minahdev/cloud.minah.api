from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.adapter.outbound.orm.community_orm import CommunityComment, CommunityPost, CommunityPostCheer
from inbody.app.dtos.community_dto import MediaItemDto, PostCreateCommand, PostDto
from inbody.app.ports.output.community_post_repository import CommunityPostRepository


def _media_to_dto(raw: list | None) -> list[MediaItemDto]:
    if not raw:
        return []
    return [MediaItemDto(url=m.get("url", ""), type=m.get("type", "image")) for m in raw]


def _to_dto(
    row: CommunityPost,
    cheer_count: int = 0,
    comment_count: int = 0,
    cheered_by_me: bool = False,
) -> PostDto:
    return PostDto(
        id=str(row.id),
        author_id=str(row.author_user_id),
        workout_type=row.workout_type or "",
        content=row.content or "",
        created_at=row.created_at.isoformat() if row.created_at else "",
        cheer_count=cheer_count,
        comment_count=comment_count,
        cheered_by_me=cheered_by_me,
        media=_media_to_dto(row.media_json),
        distance_km=row.distance_km,
        duration_min=row.duration_min,
        calories=row.calories,
    )


class CommunityPostPgRepository(CommunityPostRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[PostDto]:
        stmt = select(CommunityPost).order_by(CommunityPost.created_at.desc())
        result = await self._session.execute(stmt)
        rows = list(result.scalars().all())
        if not rows:
            return []
        post_ids = [r.id for r in rows]

        cheer_stmt = (
            select(CommunityPostCheer.post_id, func.count())
            .where(CommunityPostCheer.post_id.in_(post_ids))
            .group_by(CommunityPostCheer.post_id)
        )
        comment_stmt = (
            select(CommunityComment.post_id, func.count())
            .where(CommunityComment.post_id.in_(post_ids))
            .group_by(CommunityComment.post_id)
        )
        cheer_res = await self._session.execute(cheer_stmt)
        comment_res = await self._session.execute(comment_stmt)
        cheers = {int(pid): int(cnt) for pid, cnt in cheer_res.all()}
        comments = {int(pid): int(cnt) for pid, cnt in comment_res.all()}

        return [
            _to_dto(r, cheers.get(r.id, 0), comments.get(r.id, 0))
            for r in rows
        ]

    async def get(self, post_id: int) -> PostDto | None:
        stmt = select(CommunityPost).where(CommunityPost.id == post_id)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            return None
        cheer_stmt = (
            select(func.count())
            .select_from(CommunityPostCheer)
            .where(CommunityPostCheer.post_id == post_id)
        )
        comment_stmt = (
            select(func.count())
            .select_from(CommunityComment)
            .where(CommunityComment.post_id == post_id)
        )
        cheer_cnt = (await self._session.execute(cheer_stmt)).scalar_one()
        comment_cnt = (await self._session.execute(comment_stmt)).scalar_one()
        return _to_dto(row, cheer_cnt, comment_cnt)

    async def create(
        self,
        command: PostCreateCommand,
        author_user_pk: int,
        author_login_id: str,
    ) -> PostDto:
        media_json = [{"url": m.url, "type": m.type} for m in command.media] if command.media else None
        row = CommunityPost(
            author_user_id=author_user_pk,
            workout_type=command.workout_type,
            content=command.content,
            distance_km=command.distance_km,
            duration_min=command.duration_min,
            calories=command.calories,
            media_json=media_json,
            created_at=datetime.now(timezone.utc),
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _to_dto(row)
