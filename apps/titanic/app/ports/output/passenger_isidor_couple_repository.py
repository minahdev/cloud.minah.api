from __future__ import annotations

from abc import ABC, abstractmethod


class IsidorBedRepository(ABC):
    """Isidor — 객실/등급별 승객 수(구명보트 우선 참고)."""

    @abstractmethod
    async def count_by_pclass(self) -> dict[str, int]:
        ...
