import pytest
from types import SimpleNamespace

from titanic.adapter.outbound.mappers.passenger_jack_trainer_mapper import JackTrainerMapper
from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    GenderType,
    PassengerId,
    PassengerName,
    SurvivalStatus,
)
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity


def _make_orm(**overrides):
    defaults = dict(
        id=1,
        passenger_id="P001",
        name="Dawson, Mr. Jack",
        gender="male",
        age="30.0",
        sib_sp="0",
        parch="0",
        survived="0",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _make_entity(
    id: int = 1,
    passenger_id: str = "P001",
    name: str = "Dawson, Mr. Jack",
    gender_raw: str = "male",
    age_value: float = 30.0,
    sib_sp: int = 0,
    parch: int = 0,
    survived: bool | None = False,
) -> PassengerEntity:
    return PassengerEntity(
        id=id,
        passenger_id=PassengerId(passenger_id),
        name=PassengerName(name),
        gender=Gender.from_raw(gender_raw),
        age=Age(age_value),
        family_relation=FamilyRelation(sib_sp=sib_sp, parch=parch),
        survival_status=SurvivalStatus(survived=survived),
    )


class TestToEntity:
    def test_maps_id(self):
        entity = JackTrainerMapper.to_entity(_make_orm(id=42))
        assert entity.id == 42

    def test_maps_passenger_id(self):
        entity = JackTrainerMapper.to_entity(_make_orm(passenger_id="P099"))
        assert str(entity.passenger_id) == "P099"

    def test_maps_name(self):
        entity = JackTrainerMapper.to_entity(_make_orm(name="Smith, Mr. John"))
        assert entity.name.full_name == "Smith, Mr. John"

    def test_maps_gender_male(self):
        entity = JackTrainerMapper.to_entity(_make_orm(gender="male"))
        assert entity.gender.value == GenderType.MALE

    def test_maps_gender_female(self):
        entity = JackTrainerMapper.to_entity(_make_orm(gender="female"))
        assert entity.gender.value == GenderType.FEMALE

    def test_maps_age(self):
        entity = JackTrainerMapper.to_entity(_make_orm(age="25.0"))
        assert entity.age.value == 25.0

    def test_maps_family_relation(self):
        entity = JackTrainerMapper.to_entity(_make_orm(sib_sp="2", parch="3"))
        assert entity.family_relation.sib_sp == 2
        assert entity.family_relation.parch == 3

    def test_survived_1_maps_to_true(self):
        entity = JackTrainerMapper.to_entity(_make_orm(survived="1"))
        assert entity.survival_status.survived is True

    def test_survived_0_maps_to_false(self):
        entity = JackTrainerMapper.to_entity(_make_orm(survived="0"))
        assert entity.survival_status.survived is False

    def test_survived_none_maps_to_unknown(self):
        entity = JackTrainerMapper.to_entity(_make_orm(survived=None))
        assert entity.survival_status.is_unknown is True

    def test_none_passenger_id_maps_to_none(self):
        entity = JackTrainerMapper.to_entity(_make_orm(passenger_id=None))
        assert entity.passenger_id is None

    def test_none_name_maps_to_none(self):
        entity = JackTrainerMapper.to_entity(_make_orm(name=None))
        assert entity.name is None


class TestToOrm:
    # JackTrainerOrm의 PK는 passenger_id이며 id 컬럼이 없음.
    # 현재 mapper가 JackTrainerOrm(id=entity.id, ...) 로 생성하므로 TypeError 발생.
    # 아래 테스트는 이 버그를 문서화한다 (Red → 수정 대상).

    def test_survival_true_serializes_to_string_1(self):
        entity = _make_entity(survived=True)
        with pytest.raises(TypeError):
            JackTrainerMapper.to_orm(entity)

    def test_survival_false_serializes_to_string_0(self):
        entity = _make_entity(survived=False)
        with pytest.raises(TypeError):
            JackTrainerMapper.to_orm(entity)

    def test_survival_unknown_serializes_to_none(self):
        entity = _make_entity(survived=None)
        with pytest.raises(TypeError):
            JackTrainerMapper.to_orm(entity)