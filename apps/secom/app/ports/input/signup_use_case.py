from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SignupUseCase(ABC):

    @abstractmethod
    async def receive_uploaded_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        ...
        pass