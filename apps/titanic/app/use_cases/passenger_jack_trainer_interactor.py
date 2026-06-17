from __future__ import annotations
from typing import Any

import numpy as np
import pandas as pd
from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import (
    JackTrainerSchema
)
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse, JackTrainerQuery
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort
from titanic.app.use_cases.passenger_rose_model_interactor import build_all_strategies

import logging

logger = logging.getLogger(__name__)


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerPort):
        self.repository = repository
        self._trained_strategies: dict = {}

    async def train_model(self, train_set: pd.DataFrame) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")

        train = train_set.copy()

        # 1. Label 분리 (빈 문자열·NaN 제거)
        train["survived"] = pd.to_numeric(train["survived"], errors="coerce")
        train = train.dropna(subset=["survived"])
        y_label = train["survived"].astype(int).tolist()
        train = train.drop("survived", axis=1)

        # 2. 성별 Nominal 변환 (female=1, male=0)
        train["gender"] = train["gender"].map({"male": 0, "female": 1})

        # 3. 나이 결측치 처리
        train["age"] = pd.to_numeric(train["age"], errors="coerce").fillna(29.7)

        # 4. 승선항 Nominal 변환
        train["embarked"] = train["embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3}).fillna(1)

        # 5. 요금 처리
        train["fare"] = pd.to_numeric(train["fare"], errors="coerce").fillna(32.2)

        # 6. pclass 처리
        train["pclass"] = pd.to_numeric(train["pclass"], errors="coerce").fillna(3)

        # 7. sib_sp, parch 처리
        train["sib_sp"] = pd.to_numeric(train["sib_sp"], errors="coerce").fillna(0)
        train["parch"] = pd.to_numeric(train["parch"], errors="coerce").fillna(0)

        # 8. 불필요 컬럼 드롭
        drop_cols = ["passenger_id", "name", "ticket", "cabin"]
        train = train.drop(columns=[c for c in drop_cols if c in train.columns])

        X_train: list[list[float]] = train.values.tolist()

        # 9. 로즈의 10개 전략으로 학습
        self._trained_strategies = {}
        trained_names = []
        for key, StrategyClass in build_all_strategies().items():
            strategy = StrategyClass()
            try:
                strategy.fit(X_train, y_label)
                self._trained_strategies[key] = strategy
                trained_names.append(key)
                logger.info(f"[JackTrainerInteractor] {key} 학습 완료")
            except Exception as e:
                logger.warning(f"[JackTrainerInteractor] {key} 학습 실패 | error={e}")

        return {
            "train_samples": len(X_train),
            "trained_models": trained_names,
            "trained_strategies": self._trained_strategies,
        }

    async def analyze_jack_dawson(self) -> dict[str, Any]:
        return {}

    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        return {}

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name
        ))
