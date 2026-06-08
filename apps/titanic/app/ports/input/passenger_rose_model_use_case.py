from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RoseModelUseCase(ABC):

    @abstractmethod
    async def analyze_rose_survival(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        ...