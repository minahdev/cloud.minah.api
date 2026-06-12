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
    value: GenderType

    @classmethod
    def from_raw(cls, raw: str | None) -> Gender:
        if raw is None:
            return cls(GenderType.UNKNOWN)
        mapping = {
            "male": GenderType.MALE, "m": GenderType.MALE,
            "female": GenderType.FEMALE, "f": GenderType.FEMALE,
        }
        return cls(mapping.get(raw.strip().lower(), GenderType.UNKNOWN))

    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE


@dataclass(frozen=True)
class PassengerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("빈 값: PassengerId는 비어있을 수 없습니다")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class PassengerName:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("PassengerName은 비어있을 수 없습니다")
        if len(self.value) > 200:
            raise ValueError("PassengerName은 200자를 초과할 수 없습니다")

    @property
    def full_name(self) -> str:
        return self.value

    @property
    def normalized(self) -> str:
        return self.value.strip()


@dataclass(frozen=True)
class Age:
    value: Optional[float]

    def __post_init__(self) -> None:
        if self.value is not None and not (0 <= self.value <= 120):
            raise ValueError(f"Age out of range: {self.value}")

    @classmethod
    def from_raw(cls, raw: str | None) -> Age:
        if not raw or not raw.strip():
            return cls(value=None)
        try:
            return cls(float(raw.strip()))
        except ValueError:
            raise ValueError(f"파싱 실패: Age cannot be parsed from {raw!r}")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        if self.value is None:
            return False
        return self.value < 18


@dataclass(frozen=True)
class FamilyRelation:
    sib_sp: int
    parch: int

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise ValueError(f"sib_sp must be >= 0, got {self.sib_sp}")
        if self.parch < 0:
            raise ValueError(f"parch must be >= 0, got {self.parch}")

    @classmethod
    def from_raw(cls, sib_sp: str | None, parch: str | None) -> FamilyRelation:
        def _parse(v: str | None) -> int:
            if not v or not v.strip():
                return 0
            return int(v.strip())
        return cls(sib_sp=_parse(sib_sp), parch=_parse(parch))

    @property
    def total_family_size(self) -> int:
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.total_family_size == 0


@dataclass
class SurvivalStatus:
    survived: Optional[bool]

    @classmethod
    def from_raw(cls, raw: str | None) -> SurvivalStatus:
        if not raw or not raw.strip():
            return cls(survived=None)
        mapping = {
            "1": True, "true": True, "yes": True, "survived": True,
            "0": False, "false": False, "no": False, "not_survived": False,
        }
        result = mapping.get(raw.strip().lower())
        if result is None:
            raise ValueError(f"파싱 실패: SurvivalStatus cannot be parsed from {raw!r}")
        return cls(survived=result)

    @property
    def is_unknown(self) -> bool:
        return self.survived is None


# backward compat alias — 기존 PassengerMapper 등이 SurvivedStatus를 import하므로 유지
SurvivedStatus = SurvivalStatus
