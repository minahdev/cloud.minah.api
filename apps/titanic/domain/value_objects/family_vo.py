from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FamilyRelation:
    """sib_sp + parch 임베디드 값 타입.

    두 컬럼은 다중공선성(+0.89)이 있어 개별 예측력이 낮다.
    하나의 도메인 개념(동반 가족)으로 통합해 is_alone / total_family_size 를 파생한다.
    """
    sib_sp: int
    parch: int

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise ValueError(f"sib_sp는 0 이상이어야 합니다. got: {self.sib_sp}")
        if self.parch < 0:
            raise ValueError(f"parch는 0 이상이어야 합니다. got: {self.parch}")

    @classmethod
    def from_raw(cls, sib_sp: Optional[str], parch: Optional[str]) -> "FamilyRelation":
        def _parse(v: Optional[str]) -> int:
            if not v or not str(v).strip():
                return 0
            return int(str(v).strip())
        return cls(sib_sp=_parse(sib_sp), parch=_parse(parch))

    @property
    def total_family_size(self) -> int:
        """본인 포함 총 가족 수 (sib_sp + parch + 1)."""
        return self.sib_sp + self.parch + 1

    @property
    def is_alone(self) -> bool:
        """동반 가족이 없는 단독 탑승 여부."""
        return self.total_family_size == 1

    @property
    def is_large_family(self) -> bool:
        """5인 이상 대가족 — 생존율 하락 구간."""
        return self.total_family_size >= 5

    def __str__(self) -> str:
        return f"sib_sp={self.sib_sp}, parch={self.parch}"
