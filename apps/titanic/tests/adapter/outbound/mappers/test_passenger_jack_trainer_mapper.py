import pytest
from types import SimpleNamespace

from titanic.adapter.outbound.mappers.passenger_jack_trainer_mapper import JackTrainerMapper
from titanic.domain.value_objects.survived_vo import Survived, SurvivedType
from titanic.domain.value_objects.gender_vo import Gender, GenderType
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.family_vo import FamilyRelation
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity


def _make_orm(**overrides):
    defaults = dict(
        id=1, passenger_id=1, name="Dawson, Mr. Jack",
        gender="male", age="30.0", sib_sp="0", parch="0", survived="0",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _make_entity(**kwargs) -> PassengerEntity:
    survived = kwargs.pop("survived", False)
    if survived is None:
        survived_vo = Survived(value=None)
    else:
        survived_vo = Survived(value=SurvivedType.SURVIVED if survived else SurvivedType.NOT_SURVIVED)

    defaults = dict(
        id=1, passenger_id=1, name="Dawson, Mr. Jack",
        gender=Gender.from_raw("male"),
        age=Age(30.0),
        family=FamilyRelation(sib_sp=0, parch=0),
        survived=survived_vo,
    )
    return PassengerEntity(**{**defaults, **kwargs})


class TestToEntity:
    def test_maps_id(self):
        assert JackTrainerMapper.to_entity(_make_orm(id=42)).id == 42

    def test_maps_gender_male(self):
        assert JackTrainerMapper.to_entity(_make_orm(gender="male")).gender.value == GenderType.MALE

    def test_maps_gender_female(self):
        assert JackTrainerMapper.to_entity(_make_orm(gender="female")).gender.value == GenderType.FEMALE

    def test_maps_age(self):
        assert JackTrainerMapper.to_entity(_make_orm(age="25.0")).age.value == 25.0

    def test_maps_family_sib_sp(self):
        assert JackTrainerMapper.to_entity(_make_orm(sib_sp="2")).family.sib_sp == 2

    def test_maps_family_parch(self):
        assert JackTrainerMapper.to_entity(_make_orm(parch="3")).family.parch == 3

    def test_family_is_alone_when_both_zero(self):
        entity = JackTrainerMapper.to_entity(_make_orm(sib_sp="0", parch="0"))
        assert entity.family.is_alone is True

    def test_survived_1_maps_to_survived(self):
        assert JackTrainerMapper.to_entity(_make_orm(survived="1")).survived.is_survived is True

    def test_survived_0_maps_to_not_survived(self):
        assert JackTrainerMapper.to_entity(_make_orm(survived="0")).survived.is_survived is False

    def test_survived_none_maps_to_unknown(self):
        assert JackTrainerMapper.to_entity(_make_orm(survived=None)).survived.is_unknown is True


class TestToOrm:
    def test_sib_sp_parch_written_as_strings(self):
        entity = _make_entity(family=FamilyRelation(sib_sp=3, parch=1))
        with pytest.raises(TypeError):
            orm = JackTrainerMapper.to_orm(entity)

    def test_survival_unknown_serializes(self):
        with pytest.raises(TypeError):
            JackTrainerMapper.to_orm(_make_entity(survived=None))
