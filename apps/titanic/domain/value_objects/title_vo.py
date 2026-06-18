from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TitleType(int, Enum):
    UNKNOWN = 0
    MR      = 1
    MISS    = 2
    MRS     = 3
    MASTER  = 4
    ROYAL   = 5  # Countess, Lady, Sir
    RARE    = 6  # Capt, Col, Don, Dr, Major, Rev, Jonkheer, Dona, Mme


_RAW_TO_TYPE: dict[str, TitleType] = {
    "Mr":       TitleType.MR,
    "Miss":     TitleType.MISS,
    "Ms":       TitleType.MISS,
    "Mlle":     TitleType.MISS,
    "Mrs":      TitleType.MRS,
    "Mme":      TitleType.RARE,
    "Master":   TitleType.MASTER,
    "Countess": TitleType.ROYAL,
    "Lady":     TitleType.ROYAL,
    "Sir":      TitleType.ROYAL,
    "Capt":     TitleType.RARE,
    "Col":      TitleType.RARE,
    "Don":      TitleType.RARE,
    "Dona":     TitleType.RARE,
    "Dr":       TitleType.RARE,
    "Jonkheer": TitleType.RARE,
    "Major":    TitleType.RARE,
    "Rev":      TitleType.RARE,
}


@dataclass(frozen=True)
class Title:
    """이름에서 추출한 호칭 VO. 나이 결측치 대체 및 생존율 분석 피처."""
    value: TitleType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Title":
        if not raw or not raw.strip():
            return cls(value=TitleType.UNKNOWN)
        return cls(value=_RAW_TO_TYPE.get(raw.strip(), TitleType.UNKNOWN))

    @classmethod
    def from_name(cls, full_name: str) -> "Title":
        """'Braund, Mr. Owen Harris' 에서 호칭 추출."""
        import re
        match = re.search(r",\s*([A-Za-z]+)\.", full_name)
        if not match:
            return cls(value=TitleType.UNKNOWN)
        return cls.from_raw(match.group(1))

    @property
    def is_female(self) -> bool:
        return self.value in (TitleType.MISS, TitleType.MRS)

    @property
    def is_child(self) -> bool:
        """Master = 전통적으로 남자 미성년자 호칭."""
        return self.value == TitleType.MASTER

    def __str__(self) -> str:
        return str(self.value.value)
