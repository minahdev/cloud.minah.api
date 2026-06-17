from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse, RoseModelQuery, TrainingData
from titanic.app.ports.output.passenger_rose_model_port import RoseModelPort

import logging

logger = logging.getLogger(__name__)

_EMBARKED_MAP = {"C": 0.0, "Q": 1.0, "S": 2.0}

class RoseModelRepository(RoseModelPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        logger.info(f"[RoseModelPgRepository] introduce_myself | request_data={query}")
        return RoseModelResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

    async def get_training_data(self) -> TrainingData:
        result = await self.session.execute(
            select(JackTrainerOrm, RoseModelOrm)
            .join(RoseModelOrm, RoseModelOrm.passenger_id == JackTrainerOrm.passenger_id, isouter=True)
            .where(JackTrainerOrm.survived.isnot(None))
        )
        rows = result.all()

        X: list[list[float]] = []
        y: list[int] = []
        for passenger, booking in rows:
            try:
                survived = int(passenger.survived)
            except (ValueError, TypeError):
                continue
            sex = 1.0 if passenger.gender == "male" else 0.0
            features = [
                float(booking.pclass or 3) if booking else 3.0,
                sex,
                float(passenger.age or 29.7),
                float(passenger.sib_sp or 0),
                float(passenger.parch or 0),
                float(booking.fare or 32.2) if booking else 32.2,
                _EMBARKED_MAP.get(booking.embarked if booking else "", 2.0),
            ]
            X.append(features)
            y.append(survived)

        logger.info(f"[RoseModelPgRepository] get_training_data | rows={len(y)}")
        return TrainingData(X=X, y=y)