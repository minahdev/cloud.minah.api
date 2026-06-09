from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from inbody.controllers.community_controller import CommunityController
from inbody.deps import get_community_controller
from inbody.controllers.notice_controller import NoticeController
from inbody.controllers.schedule_controller import ScheduleController
from inbody.controllers.today_story_controller import TodayStoryController
from inbody.controllers.train_log_controller import TrainLogController
from inbody.schemas.community_schema import (
    CommunityCheerRequest,
    CommunityCheerResponse,
    CommunityCommentCreate,
    CommunityCommentResponse,
    CommunityMediaUploadResponse,
    CommunityPostCreate,
    CommunityPostResponse,
)
from inbody.schemas.notice_schema import NoticeCreate, NoticeResponse
from inbody.schemas.schedule_schema import LessonPayload, LessonResponse
from inbody.schemas.today_story_schema import TodayStoryPayload, TodayStoryResponse
from inbody.schemas.train_log_schema import TrainDailyLogPayload, TrainDailyLogResponse

router = APIRouter(prefix="/inbody", tags=["inbody"])


@router.get("/today-stories", response_model=list[TodayStoryResponse])
async def list_today_stories(userId: str, db: AsyncSession = Depends(get_db)):
    return await TodayStoryController(db).list_stories(userId)


@router.get("/today-story", response_model=TodayStoryResponse | None)
async def get_today_story(
    userId: str, date: str | None = None, db: AsyncSession = Depends(get_db)
):
    return await TodayStoryController(db).get(userId, date)


@router.put("/today-story", response_model=TodayStoryResponse)
async def put_today_story(
    req: TodayStoryPayload, db: AsyncSession = Depends(get_db)
) -> TodayStoryResponse:
    return await TodayStoryController(db).save(req)


@router.get("/train-logs", response_model=list[TrainDailyLogResponse])
async def list_train_logs(userId: str, db: AsyncSession = Depends(get_db)):
    return await TrainLogController(db).list_logs(userId)


@router.get("/train-logs/day", response_model=TrainDailyLogResponse | None)
async def get_train_log_day(
    userId: str, date: str, db: AsyncSession = Depends(get_db)
):
    return await TrainLogController(db).get(userId, date)


@router.put("/train-logs", response_model=TrainDailyLogResponse)
async def put_train_log(
    req: TrainDailyLogPayload, db: AsyncSession = Depends(get_db)
) -> TrainDailyLogResponse:
    return await TrainLogController(db).save(req)


@router.get("/lessons", response_model=list[LessonResponse])
async def list_lessons(
    userId: str,
    memberUserId: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await ScheduleController(db).list_lessons(userId, memberUserId)


@router.put("/lessons", response_model=LessonResponse)
async def put_lesson(req: LessonPayload, db: AsyncSession = Depends(get_db)) -> LessonResponse:
    return await ScheduleController(db).save_lesson(req)


@router.delete("/lessons/{client_id}")
async def delete_lesson(
    client_id: str,
    userId: str,
    memberUserId: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    await ScheduleController(db).delete_lesson(userId, client_id, memberUserId)
    return {"ok": True}


@router.get("/community/posts", response_model=list[CommunityPostResponse])
async def list_community_posts(
    userId: str | None = None,
    ctrl: CommunityController = Depends(get_community_controller),
):
    return await ctrl.list_posts(userId)


@router.post("/community/posts", response_model=CommunityPostResponse)
async def create_community_post(
    req: CommunityPostCreate,
    ctrl: CommunityController = Depends(get_community_controller),
) -> CommunityPostResponse:
    return await ctrl.create_post(req)


@router.post("/community/media", response_model=CommunityMediaUploadResponse)
async def upload_community_media(
    userId: str = Form(...),
    file: UploadFile = File(...),
    ctrl: CommunityController = Depends(get_community_controller),
) -> CommunityMediaUploadResponse:
    return await ctrl.upload_media(userId, file)


@router.post("/community/posts/{post_id}/cheer", response_model=CommunityCheerResponse)
async def toggle_community_cheer(
    post_id: int,
    req: CommunityCheerRequest,
    ctrl: CommunityController = Depends(get_community_controller),
) -> CommunityCheerResponse:
    return await ctrl.toggle_cheer(post_id, req)


@router.get(
    "/community/posts/{post_id}/comments",
    response_model=list[CommunityCommentResponse],
)
async def list_community_comments(
    post_id: int,
    ctrl: CommunityController = Depends(get_community_controller),
):
    return await ctrl.list_comments(post_id)


@router.post(
    "/community/posts/{post_id}/comments",
    response_model=CommunityCommentResponse,
)
async def create_community_comment(
    post_id: int,
    req: CommunityCommentCreate,
    ctrl: CommunityController = Depends(get_community_controller),
) -> CommunityCommentResponse:
    return await ctrl.create_comment(post_id, req)


@router.get("/notices", response_model=list[NoticeResponse])
async def list_notices(db: AsyncSession = Depends(get_db)):
    return await NoticeController(db).list_notices()


@router.post("/notices", response_model=NoticeResponse)
async def create_notice(req: NoticeCreate, db: AsyncSession = Depends(get_db)) -> NoticeResponse:
    return await NoticeController(db).create_notice(req)


@router.delete("/notices/{notice_id}")
async def delete_notice(notice_id: str, userId: str, db: AsyncSession = Depends(get_db)):
    await NoticeController(db).delete_notice(userId, notice_id)
    return {"ok": True}
