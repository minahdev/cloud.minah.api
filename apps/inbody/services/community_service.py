from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.dates import iso_utc
from inbody.models.community_model import CommunityComment, CommunityPost
from inbody.repositories.community_repository import CommunityRepository
from fastapi import UploadFile

from inbody.community_media import MAX_FILES_PER_POST, CommunityMediaStorage
from inbody.schemas.community_schema import (
    CommunityCheerResponse,
    CommunityCommentCreate,
    CommunityCommentResponse,
    CommunityMediaItem,
    CommunityMediaUploadResponse,
    CommunityPostCreate,
    CommunityPostResponse,
)
from inbody.user_lookup import require_user
from secom.app.dtos.user_model import User


def _parse_media(raw: list | None) -> list[CommunityMediaItem]:
    if not raw:
        return []
    out: list[CommunityMediaItem] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        kind = item.get("type")
        if isinstance(url, str) and kind in ("image", "video"):
            out.append(CommunityMediaItem(url=url, type=kind))
    return out


def _to_response(
    row: CommunityPost,
    author_login_id: str,
    *,
    cheer_count: int = 0,
    comment_count: int = 0,
    cheered_by_me: bool = False,
) -> CommunityPostResponse:
    return CommunityPostResponse(
        id=str(row.id),
        authorId=author_login_id,
        workoutType=row.workout_type,
        content=row.content,
        createdAt=iso_utc(row.created_at),
        distanceKm=row.distance_km,
        durationMin=row.duration_min,
        calories=row.calories,
        media=_parse_media(row.media_json),
        cheerCount=cheer_count,
        commentCount=comment_count,
        cheeredByMe=cheered_by_me,
    )


def _comment_response(row: CommunityComment, author_login_id: str) -> CommunityCommentResponse:
    return CommunityCommentResponse(
        id=str(row.id),
        authorId=author_login_id,
        content=row.content,
        createdAt=iso_utc(row.created_at),
    )


class CommunityService:
    def __init__(
        self,
        session: AsyncSession,
        media_storage: CommunityMediaStorage,
    ) -> None:
        self._repo = CommunityRepository(session)
        self._session = session
        self._media_storage = media_storage

    async def _login_id_for(self, user_pk: int) -> str:
        stmt = select(User.user_id).where(User.id == user_pk)
        result = await self._session.execute(stmt)
        login = result.scalar_one_or_none()
        return login or "unknown"

    async def list_posts(self, viewer_user_id: str | None = None) -> list[CommunityPostResponse]:
        rows = await self._repo.list_all()
        if not rows:
            return []

        post_ids = [row.id for row in rows]
        cheer_counts = await self._repo.cheer_counts(post_ids)
        comment_counts = await self._repo.comment_counts(post_ids)

        viewer_pk: int | None = None
        cheered_ids: set[int] = set()
        if viewer_user_id:
            try:
                viewer = await require_user(self._session, viewer_user_id)
                viewer_pk = viewer.id
                cheered_ids = await self._repo.cheered_post_ids(viewer_pk, post_ids)
            except ValueError:
                pass

        out: list[CommunityPostResponse] = []
        for row in rows:
            login = await self._login_id_for(row.author_user_id)
            out.append(
                _to_response(
                    row,
                    login,
                    cheer_count=cheer_counts.get(row.id, 0),
                    comment_count=comment_counts.get(row.id, 0),
                    cheered_by_me=row.id in cheered_ids,
                )
            )
        return out

    async def create_post(self, payload: CommunityPostCreate) -> CommunityPostResponse:
        content = payload.content.strip()
        media = payload.media[:MAX_FILES_PER_POST]
        if not content and not media:
            raise ValueError("내용 또는 사진·동영상 중 하나는 필요합니다.")
        if len(payload.media) > MAX_FILES_PER_POST:
            raise ValueError(f"첨부는 최대 {MAX_FILES_PER_POST}개까지 가능합니다.")

        user = await require_user(self._session, payload.userId)
        media_json = [{"url": m.url, "type": m.type} for m in media]
        row = await self._repo.create(
            user.id,
            payload.workoutType.strip() or "기타",
            content,
            payload.distanceKm,
            payload.durationMin,
            payload.calories,
            media_json if media_json else None,
        )
        return _to_response(row, user.user_id)

    async def upload_media(
        self, user_id: str, file: UploadFile
    ) -> CommunityMediaUploadResponse:
        await require_user(self._session, user_id)
        saved = await self._media_storage.save(file)
        return CommunityMediaUploadResponse(**saved)

    async def toggle_cheer(self, post_id: int, user_id: str) -> CommunityCheerResponse:
        user = await require_user(self._session, user_id)
        post = await self._repo.get_post(post_id)
        if post is None:
            raise ValueError("게시물을 찾을 수 없습니다.")
        cheered = await self._repo.toggle_cheer(post_id, user.id)
        counts = await self._repo.cheer_counts([post_id])
        return CommunityCheerResponse(
            cheerCount=counts.get(post_id, 0),
            cheeredByMe=cheered,
        )

    async def list_comments(self, post_id: int) -> list[CommunityCommentResponse]:
        post = await self._repo.get_post(post_id)
        if post is None:
            raise ValueError("게시물을 찾을 수 없습니다.")
        rows = await self._repo.list_comments(post_id)
        out: list[CommunityCommentResponse] = []
        for row in rows:
            login = await self._login_id_for(row.author_user_id)
            out.append(_comment_response(row, login))
        return out

    async def create_comment(
        self, post_id: int, payload: CommunityCommentCreate
    ) -> CommunityCommentResponse:
        user = await require_user(self._session, payload.userId)
        post = await self._repo.get_post(post_id)
        if post is None:
            raise ValueError("게시물을 찾을 수 없습니다.")
        row = await self._repo.create_comment(
            post_id, user.id, payload.content.strip()
        )
        return _comment_response(row, user.user_id)
