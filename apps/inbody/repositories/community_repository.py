from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.models.community_model import CommunityComment, CommunityPost, CommunityPostCheer


class CommunityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[CommunityPost]:
        stmt = select(CommunityPost).order_by(CommunityPost.created_at.desc())
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_post(self, post_id: int) -> CommunityPost | None:
        stmt = select(CommunityPost).where(CommunityPost.id == post_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        author_user_id: int,
        workout_type: str,
        content: str,
        distance_km: float | None,
        duration_min: int | None,
        calories: int | None,
        media_json: list | None,
    ) -> CommunityPost:
        row = CommunityPost(
            author_user_id=author_user_id,
            workout_type=workout_type,
            content=content,
            distance_km=distance_km,
            duration_min=duration_min,
            calories=calories,
            media_json=media_json or None,
            created_at=datetime.now(timezone.utc),
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return row

    async def cheer_counts(self, post_ids: list[int]) -> dict[int, int]:
        if not post_ids:
            return {}
        stmt = (
            select(CommunityPostCheer.post_id, func.count())
            .where(CommunityPostCheer.post_id.in_(post_ids))
            .group_by(CommunityPostCheer.post_id)
        )
        result = await self._session.execute(stmt)
        return {int(pid): int(cnt) for pid, cnt in result.all()}

    async def comment_counts(self, post_ids: list[int]) -> dict[int, int]:
        if not post_ids:
            return {}
        stmt = (
            select(CommunityComment.post_id, func.count())
            .where(CommunityComment.post_id.in_(post_ids))
            .group_by(CommunityComment.post_id)
        )
        result = await self._session.execute(stmt)
        return {int(pid): int(cnt) for pid, cnt in result.all()}

    async def cheered_post_ids(self, user_id: int, post_ids: list[int]) -> set[int]:
        if not post_ids:
            return set()
        stmt = select(CommunityPostCheer.post_id).where(
            CommunityPostCheer.user_id == user_id,
            CommunityPostCheer.post_id.in_(post_ids),
        )
        result = await self._session.execute(stmt)
        return {int(pid) for (pid,) in result.all()}

    async def toggle_cheer(self, post_id: int, user_id: int) -> bool:
        stmt = select(CommunityPostCheer).where(
            CommunityPostCheer.post_id == post_id,
            CommunityPostCheer.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            await self._session.delete(existing)
            await self._session.commit()
            return False
        self._session.add(
            CommunityPostCheer(
                post_id=post_id,
                user_id=user_id,
                created_at=datetime.now(timezone.utc),
            )
        )
        await self._session.commit()
        return True

    async def list_comments(self, post_id: int) -> list[CommunityComment]:
        stmt = (
            select(CommunityComment)
            .where(CommunityComment.post_id == post_id)
            .order_by(CommunityComment.created_at.asc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create_comment(
        self, post_id: int, author_user_id: int, content: str
    ) -> CommunityComment:
        row = CommunityComment(
            post_id=post_id,
            author_user_id=author_user_id,
            content=content,
            created_at=datetime.now(timezone.utc),
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return row
