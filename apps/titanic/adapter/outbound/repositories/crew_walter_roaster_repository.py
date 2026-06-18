from __future__ import annotations

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_port import WalterRoasterPort

import logging
logger = logging.getLogger(__name__)

class WalterRoasterRepository(WalterRoasterPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    
    async def get_train_set(self) -> pd.DataFrame:
        '''전체 승객 데이터를 데이터프레임으로 변환 (survived NULL 포함)'''
        result = await self.session.execute(
            select(JackTrainerOrm, RoseModelOrm)
            .join(RoseModelOrm, RoseModelOrm.passenger_id == JackTrainerOrm.passenger_id, isouter=True)
        )
        rows = result.all()
        return pd.DataFrame([
            {
                "passenger_id": p.passenger_id,
                "name": p.name,
                "gender": p.gender,
                "age": p.age,
                "sib_sp": p.sib_sp,
                "parch": p.parch,
                "survived": p.survived,
                "pclass": b.pclass if b else None,
                "ticket": b.ticket if b else None,
                "fare": b.fare if b else None,
                "cabin": b.cabin if b else None,
                "embarked": b.embarked if b else None,
            }
            for p, b in rows
        ])

    async def get_test_set(self) -> pd.DataFrame:
        '''Survived 컬럼이 없는 데이터 전체를 데이터프레임으로 변환'''
        result = await self.session.execute(
            select(JackTrainerOrm, RoseModelOrm)
            .join(RoseModelOrm, RoseModelOrm.passenger_id == JackTrainerOrm.passenger_id, isouter=True)
            .where(
                (JackTrainerOrm.survived.is_(None)) |
                (JackTrainerOrm.survived == "")
            )
        )
        rows = result.all()
        return pd.DataFrame([
            {
                "passenger_id": p.passenger_id,
                "name": p.name,
                "gender": p.gender,
                "age": p.age,
                "sib_sp": p.sib_sp,
                "parch": p.parch,
                "survived": p.survived,
                "pclass": b.pclass if b else None,
                "ticket": b.ticket if b else None,
                "fare": b.fare if b else None,
                "cabin": b.cabin if b else None,
                "embarked": b.embarked if b else None,\
            }
            for p, b in rows
        ])



    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        
        '''월터의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[WalterRoasterPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: WalterRoasterResponse = WalterRoasterResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response