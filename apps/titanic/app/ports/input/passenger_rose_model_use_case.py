from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema, RosePredictSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse, PredictResponse

class RoseModelUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        pass

    @abstractmethod
    def set_strategy(self, strategy: SurvivalModelStrategy) -> None:
        """런타임에 예측 알고리즘 교체"""
        ...

    @abstractmethod
    async def analyze_rose_survival(self) -> dict[str, Any]:
        """현재 전략 정보 및 전체 알고리즘 목록 반환"""
        ...

    @abstractmethod
    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        """현재 전략으로 승객 생존 예측 (fit() 선행 필요)"""
        ...


class SurvivalModelStrategy(ABC):
    """생존 예측 알고리즘 출력 포트 (Strategy)

    앱 레이어가 ML 라이브러리를 호출하는 인터페이스.
    구상 구현체는 adapter/outbound/ml/survival_strategies.py 에 위치한다.
    """

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def fit(self, X: list[list[float]], y: list[int]) -> None: ...

    @abstractmethod
    def predict(self, X: list[list[float]]) -> list[int]: ...

    @abstractmethod
    def predict_proba(self, X: list[list[float]]) -> list[float]: ...