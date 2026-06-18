from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EmbarkedPort(Enum):
    CHERBOURG   = "C"       # 셰르부르
    QUEENSTOWN  = "Q"       # 퀸즈타운
    SOUTHAMPTON = "S"       # 사우샘프턴 (탑승자 최다)
    UNKNOWN     = "unknown"


@dataclass(frozen=True)
class Embarked:
    """embarked 컬럼 VO. nominal 척도. C=셰르부르, Q=퀸즈타운, S=사우샘프턴."""
    value: EmbarkedPort

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Embarked":
        if not raw or not raw.strip():
            return cls(value=EmbarkedPort.UNKNOWN)
        mapping = {
            "c": EmbarkedPort.CHERBOURG,   "cherbourg":   EmbarkedPort.CHERBOURG,
            "q": EmbarkedPort.QUEENSTOWN,  "queenstown":  EmbarkedPort.QUEENSTOWN,
            "s": EmbarkedPort.SOUTHAMPTON, "southampton": EmbarkedPort.SOUTHAMPTON,
        }
        port = mapping.get(raw.strip().lower())
        if port is None:
            raise ValueError(f"Embarked 유효하지 않은 값: '{raw}'")
        return cls(value=port)

    @property
    def is_unknown(self) -> bool:
        return self.value == EmbarkedPort.UNKNOWN

    @property
    def port_name(self) -> str:
        names = {
            EmbarkedPort.CHERBOURG:   "Cherbourg",
            EmbarkedPort.QUEENSTOWN:  "Queenstown",
            EmbarkedPort.SOUTHAMPTON: "Southampton",
            EmbarkedPort.UNKNOWN:     "Unknown",
        }
        return names[self.value]

    def __str__(self) -> str:
        return self.value.value
