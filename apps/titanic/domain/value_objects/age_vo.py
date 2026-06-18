from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Age:
    """age 컬럼 VO. ratio 척도. 1세 미만 영유아는 소수점(0.5 등)으로 기록. None = 미기재."""
    value: Optional[float]

    def __post_init__(self) -> None:
        if self.value is not None and not (0 <= self.value <= 120):
            raise ValueError(f"Age out of range: {self.value}")

    @classmethod
    def unknown(cls) -> "Age":
        return cls(value=None)

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Age":
        if not raw or not raw.strip():
            return cls.unknown()
        try:
            return cls(value=float(raw.strip()))
        except ValueError:
            raise ValueError(f"파싱 실패: Age cannot be parsed from {raw!r}")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        return False if self.value is None else self.value < 18

    def __str__(self) -> str:
        return "unknown" if self.value is None else str(self.value)
