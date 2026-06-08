from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IsidorCoupleUseCase(ABC):

    @abstractmethod
    async def get_couple_survival(self) -> dict[str, Any]:
        ...
