from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from titanic.domain.value_objects import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    PassengerName,
    SurvivedStatus,
)


@dataclass
class Passenger:
    """
    Passenger Aggregate Root.

    불변식(invariant)
    - passenger_id, name 은 반드시 존재해야 한다.
    - 나머지 속성은 데이터 미기재(unknown/None)를 도메인 VO가 흡수한다.
    - ORM / 인프라 타입은 이 클래스에 노출되지 않는다.
    """

    passenger_id:    PassengerId
    name:            PassengerName
    gender:          Gender          # UNKNOWN = nullable raw
    age:             Age             # value=None = nullable raw
    family_relation: FamilyRelation  # sib_sp/parch 각각 None 가능
    survived:        SurvivedStatus  # UNKNOWN = nullable raw

    # ── 팩토리 ────────────────────────────────────────────────────────────────

    @classmethod
    def reconstitute(
        cls,
        *,
        passenger_id: str | None,
        name:         str | None,
        gender:       str | None,
        age:          str | None,
        sib_sp:       str | None,
        parch:        str | None,
        survived:     str | None,
    ) -> Passenger:
        """
        Repository가 DB 레코드를 Entity로 복원할 때 사용.
        필수 필드 누락은 여기서 ValueError 로 조기 실패(fail-fast).
        """
        return cls(
            passenger_id=PassengerId.from_raw(passenger_id),  # None → 즉시 실패
            name=PassengerName.from_raw(name),                 # None → 즉시 실패
            gender=Gender.from_raw(gender),
            age=Age.from_raw(age),
            family_relation=FamilyRelation.from_raw(sib_sp, parch),
            survived=SurvivedStatus.from_raw(survived),
        )

    # ── 도메인 행위 ───────────────────────────────────────────────────────────

    def mark_survived(self) -> None:
        self.survived = SurvivedStatus.SURVIVED

    def mark_not_survived(self) -> None:
        self.survived = SurvivedStatus.NOT_SURVIVED

    # ── 쿼리 프로퍼티 ─────────────────────────────────────────────────────────

    @property
    def is_traveling_alone(self) -> Optional[bool]:
        return self.family_relation.is_alone

    @property
    def is_minor(self) -> Optional[bool]:
        return self.age.is_minor

    # ── 동일성 ────────────────────────────────────────────────────────────────

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Passenger):
            return NotImplemented
        return self.passenger_id == other.passenger_id

    def __hash__(self) -> int:
        return hash(self.passenger_id)