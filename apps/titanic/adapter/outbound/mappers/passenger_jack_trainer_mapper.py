from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PassengerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import Passenger, PassengerEntity
from titanic.domain.value_objects import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    PassengerName,
    SurvivedStatus,
)
from titanic.domain.value_objects.passenger_jack_trainer_vo import SurvivalStatus


class PassengerJackTrainerMapper:
    """PassengerOrm(DB) ↔ Passenger(Domain Entity) — Jack Trainer 컨텍스트."""

    @staticmethod
    def to_entity(orm: PassengerOrm) -> Passenger:
        return Passenger.reconstitute(
            passenger_id=orm.passenger_id,
            name=orm.name,
            gender=orm.gender,
            age=orm.age,
            sib_sp=orm.sib_sp,
            parch=orm.parch,
            survived=orm.survived,
        )

    @staticmethod
    def to_orm(entity: Passenger) -> PassengerOrm:
        return PassengerOrm(
            passenger_id=str(entity.passenger_id.value),
            name=entity.name.value,
            gender=entity.gender.value,
            age=str(entity.age.value) if entity.age.value is not None else None,
            sib_sp=str(entity.family_relation.sib_sp) if entity.family_relation.sib_sp is not None else None,
            parch=str(entity.family_relation.parch) if entity.family_relation.parch is not None else None,
            survived=entity.survived.value,
        )


class JackTrainerMapper:
    """PassengerOrm(DB) ↔ PassengerEntity(Domain) — Jack Trainer 신규 설계."""

    @staticmethod
    def to_entity(orm) -> PassengerEntity:
        return PassengerEntity(
            id=orm.id,
            passenger_id=PassengerId(orm.passenger_id) if orm.passenger_id else None,
            name=PassengerName(orm.name) if orm.name else None,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            family_relation=FamilyRelation.from_raw(orm.sib_sp, orm.parch),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    @staticmethod
    def to_orm(entity: PassengerEntity) -> PassengerOrm:
        # BUG: JackTrainerOrm has no 'id' column → TypeError (documented, fix pending)
        return PassengerOrm(
            id=entity.id,
            passenger_id=str(entity.passenger_id) if entity.passenger_id else None,
            name=entity.name.full_name if entity.name else None,
            gender=entity.gender.value.value if entity.gender else None,
            age=str(entity.age.value) if entity.age.value is not None else None,
            sib_sp=str(entity.family_relation.sib_sp),
            parch=str(entity.family_relation.parch),
            survived=str(int(entity.survival_status.survived)) if entity.survival_status.survived is not None else None,
        )
