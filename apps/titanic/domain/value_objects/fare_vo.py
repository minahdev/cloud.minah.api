from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Fare:
    """fare 컬럼 VO. ratio 척도: 0 이상의 실수. None = 미기재.

    pclass·cabin과 결합해 선박 내 위치와 사회적 지위를 추정하는 핵심 피처.
    """
    value: Optional[float]

    def __post_init__(self) -> None:
        if self.value is not None and self.value < 0:
            raise ValueError(f"Fare는 0 이상이어야 합니다. got: {self.value}")

    @classmethod
    def unknown(cls) -> "Fare":
        return cls(value=None)

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Fare":
        if not raw or not raw.strip():
            return cls.unknown()
        try:
            return cls(value=float(raw.strip()))
        except ValueError:
            raise ValueError(f"Fare 파싱 실패: {raw!r}")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_free(self) -> bool:
        return self.value is not None and self.value == 0.0

    def __str__(self) -> str:
        return "unknown" if self.value is None else f"{self.value:.4f}"
