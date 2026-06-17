from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema, RosePredictSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse, RoseModelQuery, PredictCommand, PredictResponse
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_port import RoseModelPort

import logging

logger = logging.getLogger(__name__)

def build_all_strategies() -> dict[str, type[SurvivalModelStrategy]]:
    """구상 전략 레지스트리 — 순환 임포트 방지를 위해 함수로 지연 로딩"""
    from titanic.adapter.outbound.orm.passenger_rose_model_strategies import (
        CatBoostStrategy,
        DecisionTreeStrategy,
        KNNStrategy,
        LightGBMStrategy,
        LogisticRegressionStrategy,
        NaiveBayesStrategy,
        PCAKMeansStrategy,
        RandomForestStrategy,
        SVMStrategy,
        XGBoostStrategy,
    )
    return {
        "xgboost":            XGBoostStrategy,
        "randomforest":       RandomForestStrategy,
        "lightgbm":           LightGBMStrategy,
        "catboost":           CatBoostStrategy,
        "logisticregression": LogisticRegressionStrategy,
        "decisiontree":       DecisionTreeStrategy,
        "svm":                SVMStrategy,
        "knn":                KNNStrategy,
        "naivebayes":         NaiveBayesStrategy,
        "pca_kmeans":         PCAKMeansStrategy,
    }


class RoseModelInteractor(RoseModelUseCase):

    def __init__(
        self,
        repository: RoseModelPort,
        strategy: SurvivalModelStrategy | None = None,
    ) -> None:
        self.repository = repository
        if strategy is None:
            from titanic.adapter.outbound.orm.passenger_rose_model_strategies import RandomForestStrategy
            strategy = RandomForestStrategy()
        self._strategy: SurvivalModelStrategy = strategy

    # ── Strategy Pattern ────────────────────────────────────────────────────────

    def set_strategy(self, strategy: SurvivalModelStrategy) -> None:
        self._strategy = strategy

    async def analyze_rose_survival(self) -> dict[str, Any]:
        return {
            "current_strategy": self._strategy.name,
            "current_description": self._strategy.description,
            "available_strategies": [
                {"rank": i + 1, "key": key, "name": cls().name, "description": cls().description}
                for i, (key, cls) in enumerate(build_all_strategies().items())
            ],
        }

    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        features = _extract_features(passenger_data)
        try:
            prediction = self._strategy.predict([features])[0]
            proba = self._strategy.predict_proba([features])[0]
        except Exception:
            raise RuntimeError(
                f"'{self._strategy.name}' 모델이 학습되지 않았습니다. "
                "predict_survival() 호출 전에 strategy.fit(X, y)를 먼저 실행하세요."
            )
        return {
            "strategy": self._strategy.name,
            "survived": bool(prediction),
            "survival_probability": round(proba, 4),
            "passenger": passenger_data,
        }

    # ── Other Use Cases ─────────────────────────────────────────────────────────

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        return await self.repository.introduce_myself(RoseModelQuery(
            id=schema.id,
            name=schema.name,
        ))


def _extract_features(data: dict[str, Any]) -> list[float]:
    """승객 데이터 dict → 수치 피처 [pclass, gender, age, sib_sp, parch, fare]

    피처 순서: titanic-algorithm.md 기준 핵심 6개 변수
    - gender: female=1, male=0 (nominal → binary 인코딩)
    - pclass, age, sib_sp, parch, fare: ratio 척도 수치형
    """
    gender = 1.0 if str(data.get("gender", "male")).lower() == "female" else 0.0
    return [
        float(data.get("pclass", 3)),
        gender,
        float(data.get("age", 30)),
        float(data.get("sib_sp", 0)),
        float(data.get("parch", 0)),
        float(data.get("fare", 32.0)),
    ]