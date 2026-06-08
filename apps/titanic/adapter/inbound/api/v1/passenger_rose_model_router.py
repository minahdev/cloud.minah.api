from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import WalterPgRepository
from titanic.app.use_cases.passenger_cal_tester_interactor import CaledonValidation
from titanic.app.use_cases.crew_walter_roaster_interactor import WalterQuery

'''
로즈 드윗 부카터 (Rose DeWitt Bukater)
상류층의 답답함에서 벗어나고자 하는 의지, 그리고
영화의 핵심 매개체인 '다이아몬드'와 관련된 키워드입니다.
'''

rose_model_router = APIRouter(prefix="/titanic/rose", tags=["rose"])


@rose_model_router.get("/myself")
async def introduce_myself():
    return {"character": "Rose DeWitt Bukater", "role": "model", "memo": "1등석 여성 생존자. ML 모델 결과 분석·조회 담당"}