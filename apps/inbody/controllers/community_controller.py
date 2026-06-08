from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.community_media import CommunityMediaStorage
from inbody.schemas.community_schema import (
    CommunityCheerRequest,
    CommunityCheerResponse,
    CommunityCommentCreate,
    CommunityCommentResponse,
    CommunityMediaUploadResponse,
    CommunityPostCreate,
    CommunityPostResponse,
)
from inbody.services.community_service import CommunityService


class CommunityController:
    def __init__(
        self,
        session: AsyncSession,
        media_storage: CommunityMediaStorage,
    ) -> None:
        self._service = CommunityService(session, media_storage)

    async def list_posts(self, viewer_user_id: str | None = None) -> list[CommunityPostResponse]:
        return await self._service.list_posts(viewer_user_id)

    async def create_post(self, payload: CommunityPostCreate) -> CommunityPostResponse:
        try:
            return await self._service.create_post(payload)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def upload_media(
        self, user_id: str, file: UploadFile
    ) -> CommunityMediaUploadResponse:
        try:
            return await self._service.upload_media(user_id, file)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    async def toggle_cheer(
        self, post_id: int, payload: CommunityCheerRequest
    ) -> CommunityCheerResponse:
        try:
            return await self._service.toggle_cheer(post_id, payload.userId)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    async def list_comments(self, post_id: int) -> list[CommunityCommentResponse]:
        try:
            return await self._service.list_comments(post_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    async def create_comment(
        self, post_id: int, payload: CommunityCommentCreate
    ) -> CommunityCommentResponse:
        try:
            return await self._service.create_comment(post_id, payload)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
