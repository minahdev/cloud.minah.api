from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SurvivedType(int, Enum):
    SURVIVED     = 1
    NOT_SURVIVED = 0


@dataclass(frozen=True)
class Survived:
    """survived 컬럼 VO. 0 = 사망, 1 = 생존. None = 미기재(test.csv)."""
    value: Optional[SurvivedType]

    @classmethod
    def unknown(cls) -> "Survived":
        return cls(value=None)

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Survived":
        if not raw or not raw.strip():
            return cls.unknown()
        mapping = {
            "1": SurvivedType.SURVIVED, "true": SurvivedType.SURVIVED, "yes": SurvivedType.SURVIVED,
            "0": SurvivedType.NOT_SURVIVED, "false": SurvivedType.NOT_SURVIVED, "no": SurvivedType.NOT_SURVIVED,
        }
        result = mapping.get(raw.strip().lower())
        if result is None:
            raise ValueError(f"Survived 유효하지 않은 값: '{raw}'")
        return cls(value=result)

    @property
    def is_survived(self) -> bool:
        return self.value == SurvivedType.SURVIVED

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    def __str__(self) -> str:
        return "unknown" if self.value is None else str(self.value.value)
