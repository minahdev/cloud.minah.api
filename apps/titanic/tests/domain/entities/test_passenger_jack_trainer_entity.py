import pytest
from types import SimpleNamespace

from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity
from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    PassengerName,
    SurvivalStatus,
)


def _make_entity(
    id: int = 1,
    gender_raw: str | None = "male",
    age_value: float | None = 30.0,
    sib_sp: int = 0,
    parch: int = 0,
    survived: bool | None = None,
) -> PassengerEntity:
    return PassengerEntity(
        id=id,
        passenger_id=PassengerId("P001"),
        name=PassengerName("Dawson, Mr. Jack"),
        gender=Gender.from_raw(gender_raw),
        age=Age(age_value),
        family_relation=FamilyRelation(sib_sp=sib_sp, parch=parch),
        survival_status=SurvivalStatus(survived=survived),
    )


class TestIsHighRisk:
    def test_male_adult_alone_is_high_risk(self):
        assert _make_entity(gender_raw="male", age_value=30.0, sib_sp=0, parch=0).is_high_risk() is True

    def test_female_adult_alone_is_not_high_risk(self):
        assert _make_entity(gender_raw="female", age_value=30.0, sib_sp=0, parch=0).is_high_risk() is False

    def test_male_minor_alone_is_not_high_risk(self):
        assert _make_entity(gender_raw="male", age_value=15.0, sib_sp=0, parch=0).is_high_risk() is False

    def test_male_adult_with_family_is_not_high_risk(self):
        assert _make_entity(gender_raw="male", age_value=30.0, sib_sp=1, parch=0).is_high_risk() is False

    def test_unknown_gender_adult_alone_is_high_risk(self):
        # 성별 미상은 여성이 아닌 것으로 처리 → 고위험군 해당
        assert _make_entity(gender_raw=None, age_value=30.0, sib_sp=0, parch=0).is_high_risk() is True


class TestHasFamily:
    def test_has_family_when_has_siblings(self):
        assert _make_entity(sib_sp=1, parch=0).has_family() is True

    def test_has_family_when_has_children(self):
        assert _make_entity(sib_sp=0, parch=1).has_family() is True

    def test_no_family_when_alone(self):
        assert _make_entity(sib_sp=0, parch=0).has_family() is False


class TestRecordSurvival:
    def test_record_true_updates_survival_status(self):
        entity = _make_entity(survived=None)
        entity.record_survival(True)
        assert entity.survival_status.survived is True

    def test_record_false_updates_survival_status(self):
        entity = _make_entity(survived=True)
        entity.record_survival(False)
        assert entity.survival_status.survived is False


class TestEquality:
    def test_same_id_entities_are_equal(self):
        assert _make_entity(id=1) == _make_entity(id=1)

    def test_different_id_entities_are_not_equal(self):
        assert _make_entity(id=1) != _make_entity(id=2)

    def test_same_id_entities_have_same_hash(self):
        assert hash(_make_entity(id=1)) == hash(_make_entity(id=1))

    def test_entities_deduplicated_in_set_by_id(self):
        result = {_make_entity(id=1), _make_entity(id=1), _make_entity(id=2)}
        assert len(result) == 2


class TestFromOrm:
    def test_maps_all_fields_correctly(self):
        orm = SimpleNamespace(
            id=5,
            passenger_id="P005",
            name="Smith, Mrs. Jane",
            gender="female",
            age="42.0",
            sib_sp="1",
            parch="2",
            survived="1",
        )
        entity = PassengerEntity.from_orm(orm)

        assert entity.id == 5
        assert str(entity.passenger_id) == "P005"
        assert entity.gender.is_female() is True
        assert entity.age.value == 42.0
        assert entity.family_relation.sib_sp == 1
        assert entity.family_relation.parch == 2
        assert entity.survival_status.survived is True

    def test_none_optional_fields_map_to_none(self):
        orm = SimpleNamespace(
            id=1,
            passenger_id=None,
            name=None,
            gender=None,
            age=None,
            sib_sp=None,
            parch=None,
            survived=None,
        )
        entity = PassengerEntity.from_orm(orm)

        assert entity.passenger_id is None
        assert entity.name is None
        assert entity.survival_status.is_unknown is True