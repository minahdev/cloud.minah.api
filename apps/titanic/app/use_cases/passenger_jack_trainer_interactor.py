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

    async def train_model(self, X_train: list[list[float]], y_label: list[int]) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")

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
