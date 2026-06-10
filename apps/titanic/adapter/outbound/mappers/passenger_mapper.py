from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PassengerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import Passenger
from titanic.domain.value_objects import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    PassengerName,
    SurvivedStatus,
)


class PassengerMapper:
    """PassengerOrm(DB) ↔ Passenger(Domain Entity) 변환."""

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
