from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile

from inbody.adapter.inbound.api.schemas.community_schema import (
    CommunityCheerRequest,
    CommunityCheerResponse,
    CommunityCommentCreate,
    CommunityCommentResponse,
    CommunityMediaItem,
    CommunityMediaUploadResponse,
    CommunityPostCreate,
    CommunityPostResponse,
)
from inbody.app.dtos.community_dto import (
    CheerCommand,
    CommentCreateCommand,
    CommentDto,
    MediaItemDto,
    PostCreateCommand,
    PostDto,
    CheerDto,
    MediaUploadDto,
)
from inbody.app.ports.input.community_cheer_use_case import CommunityCheerUseCase
from inbody.app.ports.input.community_comment_use_case import CommunityCommentUseCase
from inbody.app.ports.input.community_media_use_case import CommunityMediaUseCase
from inbody.app.ports.input.community_post_use_case import CommunityPostUseCase
from inbody.dependencies.community_provider import (
    get_community_cheer_use_case,
    get_community_comment_use_case,
    get_community_media_use_case,
    get_community_post_use_case,
)

router = APIRouter(prefix="/inbody", tags=["inbody-community"])


def _post_dto_to_resp(dto: PostDto) -> CommunityPostResponse:
    return CommunityPostResponse(
        id=dto.id,
        authorId=dto.author_id,
        workoutType=dto.workout_type,
        content=dto.content,
        createdAt=dto.created_at,
        distanceKm=dto.distance_km,
        durationMin=dto.duration_min,
        calories=dto.calories,
        media=[CommunityMediaItem(url=m.url, type=m.type) for m in dto.media],
        cheerCount=dto.cheer_count,
        commentCount=dto.comment_count,
        cheeredByMe=dto.cheered_by_me,
    )


def _comment_dto_to_resp(dto: CommentDto) -> CommunityCommentResponse:
    return CommunityCommentResponse(
        id=dto.id,
        authorId=dto.author_id,
        content=dto.content,
        createdAt=dto.created_at,
    )


@router.get("/community/posts", response_model=list[CommunityPostResponse])
async def list_community_posts(
    use_case: CommunityPostUseCase = Depends(get_community_post_use_case),
):
    dtos = await use_case.list_posts()
    return [_post_dto_to_resp(d) for d in dtos]


@router.post("/community/posts", response_model=CommunityPostResponse)
async def create_community_post(
    req: CommunityPostCreate,
    use_case: CommunityPostUseCase = Depends(get_community_post_use_case),
) -> CommunityPostResponse:
    command = PostCreateCommand(
        user_id=req.userId,
        workout_type=req.workoutType,
        content=req.content,
        media=[MediaItemDto(url=m.url, type=m.type) for m in req.media],
        distance_km=req.distanceKm,
        duration_min=req.durationMin,
        calories=req.calories,
    )
    dto = await use_case.create_post(command)
    return _post_dto_to_resp(dto)


@router.post("/community/media", response_model=CommunityMediaUploadResponse)
async def upload_community_media(
    userId: str = Form(...),
    file: UploadFile = File(...),
    use_case: CommunityMediaUseCase = Depends(get_community_media_use_case),
) -> CommunityMediaUploadResponse:
    dto = await use_case.upload_media(userId, file)
    return CommunityMediaUploadResponse(url=dto.url, type=dto.type)


@router.post("/community/posts/{post_id}/cheer", response_model=CommunityCheerResponse)
async def toggle_community_cheer(
    post_id: int,
    req: CommunityCheerRequest,
    use_case: CommunityCheerUseCase = Depends(get_community_cheer_use_case),
) -> CommunityCheerResponse:
    command = CheerCommand(post_id=post_id, user_id=req.userId)
    dto = await use_case.toggle_cheer(command)
    return CommunityCheerResponse(cheerCount=dto.cheer_count, cheeredByMe=dto.cheered_by_me)


@router.get(
    "/community/posts/{post_id}/comments",
    response_model=list[CommunityCommentResponse],
)
async def list_community_comments(
    post_id: int,
    use_case: CommunityCommentUseCase = Depends(get_community_comment_use_case),
):
    dtos = await use_case.list_comments(post_id)
    return [_comment_dto_to_resp(d) for d in dtos]


@router.post(
    "/community/posts/{post_id}/comments",
    response_model=CommunityCommentResponse,
)
async def create_community_comment(
    post_id: int,
    req: CommunityCommentCreate,
    use_case: CommunityCommentUseCase = Depends(get_community_comment_use_case),
) -> CommunityCommentResponse:
    command = CommentCreateCommand(post_id=post_id, user_id=req.userId, content=req.content)
    dto = await use_case.create_comment(command)
    return _comment_dto_to_resp(dto)
