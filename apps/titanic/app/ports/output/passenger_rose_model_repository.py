from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RoseDiamondRepository(ABC):
    """Rose — 생존 예측 모델/학습 데이터 접근."""

    @abstractmethod
    async def get_model_info(self) -> dict[str, Any]:
        ...
