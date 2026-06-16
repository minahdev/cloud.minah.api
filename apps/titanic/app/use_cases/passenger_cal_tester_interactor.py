from __future__ import annotations
from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse, ModelScoreResult
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository
from titanic.app.use_cases.passenger_rose_model_interactor import _STRATEGY_MAP

import logging

logger = logging.getLogger(__name__)

class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTesterRepository) -> None:
        self._repository = repository

    async def test_model(self,test_set) -> dict[str, Any]:
        '''잭이 훈련시킨 모델을 1위부터 10위까지 나열하는 메소드... '''
        training = await self._repository.get_training_data()
        if not training.X:
            return {"error": "훈련 데이터 없음"}

        X_train, X_test, y_train, y_test = train_test_split(
            np.array(training.X), np.array(training.y),
            test_size=0.2, random_state=42,
        )

        scores: list[ModelScoreResult] = []
        for name, StrategyClass in _STRATEGY_MAP.items():
            strategy = StrategyClass()
            strategy.fit(X_train.tolist(), y_train.tolist())
            preds = strategy.predict(X_test.tolist())
            f1  = round(float(f1_score(y_test, preds)), 4)
            acc = round(float(accuracy_score(y_test, preds)), 4)
            scores.append(ModelScoreResult(rank=0, algorithm=name, f1_score=f1, accuracy=acc))
            logger.info(f"[CalTester] {name} | f1={f1} acc={acc}")

        ranked = sorted(scores, key=lambda s: s.f1_score, reverse=True)
        ranking = [
            {"rank": i + 1, "algorithm": s.algorithm, "f1_score": s.f1_score, "accuracy": s.accuracy}
            for i, s in enumerate(ranked)
        ]

        logger.info(f"[CalTester] 1위={ranking[0]['algorithm']} f1={ranking[0]['f1_score']}")
        return {"ranking": ranking}

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        return await self._repository.introduce_myself(CalTesterQuery(
            id=schema.id,
            name=schema.name,
        ))