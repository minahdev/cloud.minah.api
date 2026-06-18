from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class PClassType(int, Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3

@dataclass(frozen=True)
class PClass:
    value: PClassType

    @classmethod

    def from_raw(cls, raw: Optional[str]) -> "PClass":
        if raw is None or raw.strip() == "":
            raise ValueError("PClass는 필수 값입니다.")
        try:
            return cls(value=PClassType(int(raw.strip())))
        except (ValueError, KeyError):
            raise ValueError(f"PClass 유효하지 않은 값: '{raw}'")

    @property

    def is_first_class(self) -> bool:
        return self.value == PClassType.FIRST

    def __str__(self) -> str:
        return str(self.value.value)