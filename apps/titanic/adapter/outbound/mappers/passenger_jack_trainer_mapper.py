from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PassengerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity
from titanic.domain.value_objects.survived_vo import Survived
from titanic.domain.value_objects.gender_vo import Gender
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.family_vo import FamilyRelation


class JackTrainerMapper:
    """PassengerOrm(DB) ↔ PassengerEntity(Domain) — Jack Trainer."""

    @staticmethod
    def to_entity(orm) -> PassengerEntity:
        return PassengerEntity(
            id=orm.id,
            passenger_id=orm.passenger_id,
            name=orm.name,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            family=FamilyRelation.from_raw(orm.sib_sp, orm.parch),
            survived=Survived.from_raw(orm.survived),
        )

    @staticmethod
    def to_orm(entity: PassengerEntity) -> PassengerOrm:
        # BUG: JackTrainerOrm has no 'id' column → TypeError (documented, fix pending)
        return PassengerOrm(
            id=entity.id,
            passenger_id=entity.passenger_id,
            name=entity.name,
            gender=entity.gender.value.value if entity.gender else None,
            age=str(entity.age.value) if entity.age.value is not None else None,
            sib_sp=str(entity.family.sib_sp),
            parch=str(entity.family.parch),
            survived=str(entity.survived.value.value) if not entity.survived.is_unknown else None,
        )
