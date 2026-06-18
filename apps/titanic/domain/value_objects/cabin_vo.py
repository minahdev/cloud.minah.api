from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Cabin:
    """cabin 컬럼 VO. 첫 글자 = 갑판 구역(A~G, T). None = 미기재."""
    value: Optional[str]

    @classmethod
    def unknown(cls) -> "Cabin":
        return cls(value=None)

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Cabin":
        if not raw or not raw.strip():
            return cls.unknown()
        return cls(value=raw.strip())

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def deck_letter(self) -> Optional[str]:
        """갑판 구역 알파벳(A~G, T). 미기재 시 None."""
        if self.value is None:
            return None
        first = self.value[0].upper()
        return first if first.isalpha() else None

    def __str__(self) -> str:
        return self.value or "unknown"
