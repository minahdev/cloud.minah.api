from __future__ import annotations

import numpy as np
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from titanic.app.ports.input.passenger_rose_model_use_case import SurvivalModelStrategy


class XGBoostStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "XGBoost"
    @property
    def description(self) -> str: return "그래디언트 부스팅 기반 고성능 모델."
    def __init__(self) -> None: self._model = XGBClassifier(n_estimators=100, random_state=42, eval_metric="logloss", verbosity=0)
    def fit(self, X, y) -> None: self._model.fit(X, y)
    def predict(self, X) -> list[int]: return self._model.predict(X).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(X)[:, 1].tolist()


class RandomForestStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "RandomForest"
    @property
    def description(self) -> str: return "다수의 결정 트리를 결합하는 배깅 방식."
    def __init__(self) -> None: self._model = RandomForestClassifier(n_estimators=100, random_state=42)
    def fit(self, X, y) -> None: self._model.fit(X, y)
    def predict(self, X) -> list[int]: return self._model.predict(X).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(X)[:, 1].tolist()


class LightGBMStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "LightGBM"
    @property
    def description(self) -> str: return "리프 중심 트리 분할 방식."
    def __init__(self) -> None: self._model = LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
    def fit(self, X, y) -> None: self._model.fit(X, y)
    def predict(self, X) -> list[int]: return self._model.predict(X).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(X)[:, 1].tolist()


class CatBoostStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "CatBoost"
    @property
    def description(self) -> str: return "범주형 데이터 처리에 최적화된 부스팅."
    def __init__(self) -> None: self._model = CatBoostClassifier(iterations=100, random_state=42, verbose=0)
    def fit(self, X, y) -> None: self._model.fit(X, y)
    def predict(self, X) -> list[int]: return self._model.predict(X).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(X)[:, 1].tolist()


class LogisticRegressionStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "LogisticRegression"
    @property
    def description(self) -> str: return "선형 기반 이진 분류 Baseline."
    def __init__(self) -> None:
        self._scaler = StandardScaler()
        self._model = LogisticRegression(max_iter=1000, random_state=42)
    def fit(self, X, y) -> None: self._model.fit(self._scaler.fit_transform(X), y)
    def predict(self, X) -> list[int]: return self._model.predict(self._scaler.transform(X)).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class DecisionTreeStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "DecisionTree"
    @property
    def description(self) -> str: return "직관적인 규칙 기반 모델."
    def __init__(self) -> None: self._model = DecisionTreeClassifier(max_depth=5, random_state=42)
    def fit(self, X, y) -> None: self._model.fit(X, y)
    def predict(self, X) -> list[int]: return self._model.predict(X).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(X)[:, 1].tolist()


class SVMStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "SVM"
    @property
    def description(self) -> str: return "마진 최대화 결정 경계 탐색."
    def __init__(self) -> None:
        self._scaler = StandardScaler()
        self._model = SVC(kernel="rbf", probability=True, random_state=42)
    def fit(self, X, y) -> None: self._model.fit(self._scaler.fit_transform(X), y)
    def predict(self, X) -> list[int]: return self._model.predict(self._scaler.transform(X)).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class KNNStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "KNN"
    @property
    def description(self) -> str: return "K-최근접 이웃 분류."
    def __init__(self, k: int = 5) -> None:
        self._scaler = MinMaxScaler()
        self._model = KNeighborsClassifier(n_neighbors=k)
    def fit(self, X, y) -> None: self._model.fit(self._scaler.fit_transform(X), y)
    def predict(self, X) -> list[int]: return self._model.predict(self._scaler.transform(X)).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class NaiveBayesStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "NaiveBayes"
    @property
    def description(self) -> str: return "베이즈 정리 조건부 확률 기반 분류."
    def __init__(self) -> None: self._model = GaussianNB()
    def fit(self, X, y) -> None: self._model.fit(X, y)
    def predict(self, X) -> list[int]: return self._model.predict(X).tolist()
    def predict_proba(self, X) -> list[float]: return self._model.predict_proba(X)[:, 1].tolist()


class PCAKMeansStrategy(SurvivalModelStrategy):
    @property
    def name(self) -> str: return "PCA+KMeans"
    @property
    def description(self) -> str: return "PCA 차원 축소 후 K-Means 군집화."
    def __init__(self, n_components: int = 2, n_clusters: int = 2) -> None:
        self._scaler = StandardScaler()
        self._pca = PCA(n_components=n_components)
        self._kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self._cluster_to_label: dict[int, int] = {}
    def fit(self, X, y) -> None:
        X_reduced = self._pca.fit_transform(self._scaler.fit_transform(X))
        self._kmeans.fit(X_reduced)
        y_arr = np.array(y)
        for c in range(self._kmeans.n_clusters):
            mask = self._kmeans.labels_ == c
            self._cluster_to_label[c] = 1 if (float(y_arr[mask].mean()) if mask.sum() > 0 else 0.0) >= 0.5 else 0
    def predict(self, X) -> list[int]:
        X_reduced = self._pca.transform(self._scaler.transform(X))
        return [self._cluster_to_label.get(int(c), 0) for c in self._kmeans.predict(X_reduced)]
    def predict_proba(self, X) -> list[float]:
        return [float(p) for p in self.predict(X)]
