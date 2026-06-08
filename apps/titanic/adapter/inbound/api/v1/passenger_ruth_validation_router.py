from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import WalterPgRepository
from titanic.app.use_cases.crew_walter_roaster_interactor import WalterQuery

'''
루스 드윗 부카터 (Ruth DeWitt Bukater)
딸 로즈의 코르셋 끈을 강하게 조이며 상류층의 체면을 강요하던
통제욕의 상징. 1등석 승객(상류층) 조회를 담당한다.

추천 파일명: ruth_survivor_router.py
'''

ruth_survivor_router = APIRouter(prefix="/titanic/ruth", tags=["ruth"])


@ruth_survivor_router.get("/myself")
async def introduce_myself():
    return {"character": "Ruth DeWitt Bukater", "role": "survivor", "memo": "상류층 체면의 상징. 1등석 승객 필터 조회 담당"}
    