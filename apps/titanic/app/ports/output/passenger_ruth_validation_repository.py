from __future__ import annotations

from abc import ABC, abstractmethod


class RuthCorsetRepository(ABC):
    """Ruth — 승객 ID 중복·존재 확인."""

    @abstractmethod
    async def exists_passenger_id(self, passenger_id: str) -> bool:
        ...
