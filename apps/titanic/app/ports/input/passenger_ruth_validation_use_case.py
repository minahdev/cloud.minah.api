from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RuthValidationUseCase(ABC):

    @abstractmethod
    async def list_by_pclass(self, pclass: int, page: int, page_size: int) -> dict[str, Any]:
        ...
