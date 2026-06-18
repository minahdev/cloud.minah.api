from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GenderType(Enum):
    MALE    = "male"
    FEMALE  = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Gender:
    """gender 컬럼 VO. nominal 척도."""
    value: GenderType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Gender":
        if raw is None or not raw.strip():
            return cls(value=GenderType.UNKNOWN)
        mapping = {
            "male":   GenderType.MALE,   "m": GenderType.MALE,
            "female": GenderType.FEMALE, "f": GenderType.FEMALE,
        }
        return cls(value=mapping.get(raw.strip().lower(), GenderType.UNKNOWN))

    @property
    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    @property
    def is_male(self) -> bool:
        return self.value == GenderType.MALE

    @property
    def is_unknown(self) -> bool:
        return self.value == GenderType.UNKNOWN

    def __str__(self) -> str:
        return self.value.value
