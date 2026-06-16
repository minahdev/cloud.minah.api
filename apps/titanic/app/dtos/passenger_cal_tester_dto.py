from dataclasses import dataclass

@dataclass(frozen=True)
class CalTesterQuery:
    id: int
    name: str

@dataclass(frozen=True)
class CalTesterResponse:
    id: int
    name: str

@dataclass(frozen=True)
class ModelScoreResult:
    rank: int
    algorithm: str
    f1_score: float
    accuracy: float