from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MollyScalerUseCase(ABC):

    @abstractmethod
    async def scale_features(self, data: dict[str, Any]) -> dict[str, Any]:
        ...