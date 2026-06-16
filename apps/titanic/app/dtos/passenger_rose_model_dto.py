from dataclasses import dataclass, field

@dataclass(frozen=True)
class RoseModelQuery:
    id: int
    name: str

@dataclass(frozen=True)
class RoseModelResponse:
    id: int
    name: str

@dataclass(frozen=True)
class TrainingData:
    X: list[list[float]]
    y: list[int]

@dataclass(frozen=True)
class PredictCommand:
    pclass: int
    sex: str        # "male" | "female"
    age: float
    sib_sp: int
    parch: int
    fare: float
    embarked: str   # "C" | "Q" | "S"
    algorithm: str  # 아래 ALGORITHMS 참고

@dataclass(frozen=True)
class PredictResponse:
    survived: int   # 0 or 1
    algorithm: str

ALGORITHMS = [
    "xgboost", "random_forest", "lightgbm", "catboost",
    "logistic_regression", "decision_tree", "svm", "knn",
    "naive_bayes", "kmeans_pca",
]

