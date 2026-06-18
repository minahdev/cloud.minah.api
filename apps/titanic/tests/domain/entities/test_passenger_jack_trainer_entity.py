import pytest
from types import SimpleNamespace

from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity
from titanic.domain.value_objects.survived_vo import Survived, SurvivedType
from titanic.domain.value_objects.gender_vo import Gender
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.family_vo import FamilyRelation


def _make_entity(
    id: int = 1,
    gender_raw: str | None = "male",
    age_value: float | None = 30.0,
    sib_sp: int = 0,
    parch: int = 0,
    survived: bool | None = None,
) -> PassengerEntity:
    survived_vo = Survived(value=None) if survived is None else Survived(
        value=SurvivedType.SURVIVED if survived else SurvivedType.NOT_SURVIVED
    )
    return PassengerEntity(
        id=id,
        passenger_id=1,
        name="Dawson, Mr. Jack",
        gender=Gender.from_raw(gender_raw),
        age=Age(age_value),
        family=FamilyRelation(sib_sp=sib_sp, parch=parch),
        survived=survived_vo,
    )


class TestIsHighRisk:
    def test_male_adult_alone_is_high_risk(self):
        assert _make_entity(gender_raw="male", age_value=30.0, sib_sp=0, parch=0).is_high_risk() is True

    def test_female_adult_alone_is_not_high_risk(self):
        assert _make_entity(gender_raw="female", age_value=30.0).is_high_risk() is False

    def test_male_minor_alone_is_not_high_risk(self):
        assert _make_entity(gender_raw="male", age_value=15.0).is_high_risk() is False

    def test_male_adult_with_family_is_not_high_risk(self):
        assert _make_entity(gender_raw="male", age_value=30.0, sib_sp=1).is_high_risk() is False


class TestHasFamily:
    def test_has_family_when_has_siblings(self):
        assert _make_entity(sib_sp=1).has_family() is True

    def test_no_family_when_alone(self):
        assert _make_entity(sib_sp=0, parch=0).has_family() is False


class TestRecordSurvival:
    def test_record_true(self):
        entity = _make_entity(survived=None)
        entity.record_survival(True)
        assert entity.survived.is_survived is True

    def test_record_false(self):
        entity = _make_entity(survived=True)
        entity.record_survival(False)
        assert entity.survived.is_survived is False


class TestFromOrm:
    def test_maps_all_fields(self):
        orm = SimpleNamespace(
            id=5, passenger_id=5, name="Smith, Mrs. Jane",
            gender="female", age="42.0", sib_sp="1", parch="2", survived="1",
        )
        entity = PassengerEntity.from_orm(orm)
        assert entity.gender.is_female is True
        assert entity.family.sib_sp == 1
        assert entity.family.parch == 2
        assert entity.family.is_alone is False
        assert entity.survived.is_survived is True
