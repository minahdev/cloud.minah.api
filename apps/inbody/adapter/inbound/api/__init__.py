from fastapi import APIRouter

from inbody.adapter.inbound.api.v1.community_router import router as community_router
from inbody.adapter.inbound.api.v1.food_router import router as food_router
from inbody.adapter.inbound.api.v1.notice_router import router as notice_router
from inbody.adapter.inbound.api.v1.schedule_router import router as schedule_router
from inbody.adapter.inbound.api.v1.today_story_router import router as today_story_router
from inbody.adapter.inbound.api.v1.train_log_router import router as train_log_router

inbody_router = APIRouter()
inbody_router.include_router(today_story_router)
inbody_router.include_router(notice_router)
inbody_router.include_router(train_log_router)
inbody_router.include_router(schedule_router)
inbody_router.include_router(community_router)
inbody_router.include_router(food_router)
