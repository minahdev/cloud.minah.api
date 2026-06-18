from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from titanic.domain.value_objects.survived_vo import Survived, SurvivedType
from titanic.domain.value_objects.gender_vo import Gender
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.family_vo import FamilyRelation


@dataclass
class PassengerEntity:
    id: int
    passenger_id: Optional[int]
    name: Optional[str]
    gender: Gender
    age: Age
    family: FamilyRelation
    survived: Survived

    def is_high_risk(self) -> bool:
        return (
            not self.gender.is_female
            and not self.age.is_minor
            and self.family.is_alone
        )

    def has_family(self) -> bool:
        return not self.family.is_alone

    def record_survival(self, survived: bool) -> None:
        self.survived = Survived(
            value=SurvivedType.SURVIVED if survived else SurvivedType.NOT_SURVIVED
        )

    @classmethod
    def from_orm(cls, orm) -> "PassengerEntity":
        return cls(
            id=orm.id,
            passenger_id=orm.passenger_id,
            name=orm.name,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            family=FamilyRelation.from_raw(orm.sib_sp, orm.parch),
            survived=Survived.from_raw(orm.survived),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PassengerEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


Passenger = PassengerEntity
