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
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

import logging

logger = logging.getLogger(__name__)

_EMBARKED_MAP = {"C": 0.0, "Q": 1.0, "S": 2.0}


# ── Strategy ABC ──────────────────────────────────────────────────────────────
class ModelStrategy(ABC):
    @abstractmethod
    def fit(self, X: list[list[float]], y: list[int]) -> None: ...

    @abstractmethod
    def predict(self, X: list[list[float]]) -> list[int]: ...


# ── Concrete Strategies (titanic-algorithm.md TOP 10) ────────────────────────
class XGBoostStrategy(ModelStrategy):
    def __init__(self): self._m = XGBClassifier(eval_metric="logloss", random_state=42)
    def fit(self, X, y): self._m.fit(np.array(X), y)
    def predict(self, X): return self._m.predict(np.array(X)).tolist()

class RandomForestStrategy(ModelStrategy):
    def __init__(self): self._m = RandomForestClassifier(n_estimators=100, random_state=42)
    def fit(self, X, y): self._m.fit(X, y)
    def predict(self, X): return self._m.predict(X).tolist()

class LightGBMStrategy(ModelStrategy):
    def __init__(self): self._m = LGBMClassifier(random_state=42, verbose=-1)
    def fit(self, X, y): self._m.fit(X, y)
    def predict(self, X): return self._m.predict(X).tolist()

class CatBoostStrategy(ModelStrategy):
    def __init__(self): self._m = CatBoostClassifier(verbose=0, random_state=42)
    def fit(self, X, y): self._m.fit(X, y)
    def predict(self, X): return self._m.predict(X).tolist()

class LogisticRegressionStrategy(ModelStrategy):
    def __init__(self): self._m = LogisticRegression(max_iter=1000)
    def fit(self, X, y): self._m.fit(X, y)
    def predict(self, X): return self._m.predict(X).tolist()

class DecisionTreeStrategy(ModelStrategy):
    def __init__(self): self._m = DecisionTreeClassifier(random_state=42)
    def fit(self, X, y): self._m.fit(X, y)
    def predict(self, X): return self._m.predict(X).tolist()

class SVMStrategy(ModelStrategy):
    def __init__(self): self._m = SVC(kernel="rbf")
    def fit(self, X, y): self._m.fit(X, y)
    def predict(self, X): return self._m.predict(X).tolist()

class KNNStrategy(ModelStrategy):
    def __init__(self): self._m = KNeighborsClassifier(n_neighbors=5)
    def fit(self, X, y): self._m.fit(X, y)
    def predict(self, X): return self._m.predict(X).tolist()

class NaiveBayesStrategy(ModelStrategy):
    def __init__(self): self._m = GaussianNB()
    def fit(self, X, y): self._m.fit(X, y)
    def predict(self, X): return self._m.predict(X).tolist()

class KMeansPCAStrategy(ModelStrategy):
    """비지도학습: PCA 차원 축소 후 K-Means 클러스터링으로 생존 여부 예측."""
    def __init__(self):
        self._pca = PCA(n_components=2)
        self._km = KMeans(n_clusters=2, random_state=42, n_init=10)
        self._cluster_label: dict[int, int] = {}

    def fit(self, X, y):
        X_arr, y_arr = np.array(X), np.array(y)
        X_r = self._pca.fit_transform(X_arr)
        self._km.fit(X_r)
        for cid in range(2):
            mask = self._km.labels_ == cid
            self._cluster_label[cid] = int(y_arr[mask].mean() >= 0.5)

    def predict(self, X):
        X_r = self._pca.transform(np.array(X))
        return [self._cluster_label[c] for c in self._km.predict(X_r)]


_STRATEGY_MAP: dict[str, type[ModelStrategy]] = {
    "xgboost": XGBoostStrategy,
    "random_forest": RandomForestStrategy,
    "lightgbm": LightGBMStrategy,
    "catboost": CatBoostStrategy,
    "logistic_regression": LogisticRegressionStrategy,
    "decision_tree": DecisionTreeStrategy,
    "svm": SVMStrategy,
    "knn": KNNStrategy,
    "naive_bayes": NaiveBayesStrategy,
    "kmeans_pca": KMeansPCAStrategy,
}


def _to_features(s: RosePredictSchema) -> list[float]:
    return [
        float(s.pclass),
        1.0 if s.sex == "male" else 0.0,
        float(s.age),
        float(s.sib_sp),
        float(s.parch),
        float(s.fare),
        _EMBARKED_MAP.get(s.embarked, 2.0),
    ]


# ── Interactor ────────────────────────────────────────────────────────────────
class RoseModelInteractor(RoseModelUseCase):

    def __init__(self, repository: RoseModelRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        return await self._repository.introduce_myself(RoseModelQuery(
            id=schema.id,
            name=schema.name,
        ))

    async def predict_survival(self, schema: RosePredictSchema) -> PredictResponse:
        if schema.algorithm not in _STRATEGY_MAP:
            raise ValueError(f"알 수 없는 알고리즘: {schema.algorithm}. 사용 가능: {list(_STRATEGY_MAP)}")

        training = await self._repository.get_training_data()
        strategy = _STRATEGY_MAP[schema.algorithm]()
        strategy.fit(training.X, training.y)

        features = _to_features(schema)
        result = strategy.predict([features])

        logger.info(f"[RoseModelInteractor] predict_survival | algorithm={schema.algorithm} survived={result[0]}")
        return PredictResponse(survived=result[0], algorithm=schema.algorithm)
