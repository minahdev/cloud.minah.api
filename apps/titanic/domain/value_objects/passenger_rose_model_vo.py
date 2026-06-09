from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ── Gender ──────────────────────────────────────────────────────────────────

class Gender(Enum):
    MALE    = "male"
    FEMALE  = "female"
    UNKNOWN = "unknown"

    @classmethod
    def from_raw(cls, value: str | None) -> Gender:
        if not value or not value.strip():
            return cls.UNKNOWN
        mapping = {"male": cls.MALE, "m": cls.MALE,
                   "female": cls.FEMALE, "f": cls.FEMALE}
        return mapping.get(value.strip().lower(), cls.UNKNOWN)


# ── SurvivedStatus ───────────────────────────────────────────────────────────

class SurvivedStatus(Enum):
    SURVIVED     = "survived"
    NOT_SURVIVED = "not_survived"
    UNKNOWN      = "unknown"

    @classmethod
    def from_raw(cls, value: str | None) -> SurvivedStatus:
        if not value or not value.strip():
            return cls.UNKNOWN
        mapping = {
            "1": cls.SURVIVED, "true": cls.SURVIVED,
            "yes": cls.SURVIVED, "survived": cls.SURVIVED,
            "0": cls.NOT_SURVIVED, "false": cls.NOT_SURVIVED,
            "no": cls.NOT_SURVIVED, "not_survived": cls.NOT_SURVIVED,
        }
        result = mapping.get(value.strip().lower())
        if result is None:
            raise ValueError(f"Invalid survived value: {value!r}")
        return result


# ── PassengerId ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class PassengerId:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError(f"PassengerId must be positive, got {self.value}")

    @classmethod
    def from_int(cls, value: int) -> PassengerId:
        return cls(value)

    @classmethod
    def from_raw(cls, value: str | None) -> PassengerId:
        if value is None:
            raise ValueError("PassengerId must not be None")
        try:
            return cls(int(value.strip()))
        except (ValueError, AttributeError):
            raise ValueError(f"Cannot parse PassengerId: {value!r}")


# ── PassengerName ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class PassengerName:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip()
        if not stripped:
            raise ValueError("PassengerName must not be blank")
        object.__setattr__(self, "value", stripped)

    @classmethod
    def from_raw(cls, value: str | None) -> PassengerName:
        if not value or not value.strip():
            raise ValueError("PassengerName must not be blank")
        return cls(value)

    @property
    def last_name(self) -> str:
        return self.value.split(",")[0].strip() if "," in self.value else self.value

    @property
    def title(self) -> Optional[str]:
        parts = self.value.split(".")
        if len(parts) >= 2:
            segment = parts[0].split(",")
            return segment[-1].strip() if segment else None
        return None


# ── Age ──────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Age:
    """None = 미기재(unknown)."""
    value: Optional[float]

    def __post_init__(self) -> None:
        if self.value is not None and not (0 <= self.value <= 150):
            raise ValueError(f"Age out of range: {self.value}")

    @classmethod
    def unknown(cls) -> Age:
        return cls(value=None)

    @classmethod
    def from_raw(cls, value: str | None) -> Age:
        if not value or not value.strip():
            return cls.unknown()
        try:
            return cls(float(value.strip()))
        except ValueError:
            raise ValueError(f"Cannot parse Age: {value!r}")

    @property
    def is_known(self) -> bool:
        return self.value is not None

    @property
    def is_minor(self) -> Optional[bool]:
        return None if self.value is None else self.value < 18


# ── FamilyRelation ───────────────────────────────────────────────────────────

@dataclass(frozen=True)
class FamilyRelation:
    """sib_sp / parch — 빈 문자열(ORM default="")은 None으로 처리."""
    sib_sp: Optional[int]
    parch:  Optional[int]

    def __post_init__(self) -> None:
        if self.sib_sp is not None and self.sib_sp < 0:
            raise ValueError(f"sib_sp must be >= 0, got {self.sib_sp}")
        if self.parch is not None and self.parch < 0:
            raise ValueError(f"parch must be >= 0, got {self.parch}")

    @classmethod
    def unknown(cls) -> FamilyRelation:
        return cls(sib_sp=None, parch=None)

    @classmethod
    def from_raw(cls, sib_sp: str | None, parch: str | None) -> FamilyRelation:
        def _parse(v: str | None, field: str) -> Optional[int]:
            if not v or not v.strip():
                return None
            try:
                return int(v.strip())
            except ValueError:
                raise ValueError(f"Cannot parse {field}: {v!r}")

        return cls(sib_sp=_parse(sib_sp, "sib_sp"), parch=_parse(parch, "parch"))

    @property
    def family_size(self) -> Optional[int]:
        if self.sib_sp is None or self.parch is None:
            return None
        return self.sib_sp + self.parch + 1

    @property
    def is_alone(self) -> Optional[bool]:
        size = self.family_size
        return None if size is None else size == 1
