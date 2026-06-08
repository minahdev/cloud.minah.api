from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackSketchRepository(ABC):
    """Jack — 스케치용 승객 1명 조회."""

    @abstractmethod
    async def get_passenger(self, passenger_id: str) -> dict[str, Any] | None:
        ...
