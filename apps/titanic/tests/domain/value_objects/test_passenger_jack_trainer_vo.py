import pytest

from titanic.domain.value_objects.gender_vo import Gender, GenderType
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.family_vo import FamilyRelation
from titanic.domain.value_objects.survived_vo import Survived, SurvivedType


class TestGender:
    def test_from_raw_male(self):
        assert Gender.from_raw("male").value == GenderType.MALE

    def test_from_raw_female(self):
        assert Gender.from_raw("female").value == GenderType.FEMALE

    def test_from_raw_none_is_unknown(self):
        assert Gender.from_raw(None).value == GenderType.UNKNOWN

    def test_is_female_true_for_female(self):
        assert Gender.from_raw("female").is_female is True

    def test_is_female_false_for_male(self):
        assert Gender.from_raw("male").is_female is False


class TestAge:
    def test_from_raw_valid_string(self):
        assert Age.from_raw("22.5").value == 22.5

    def test_from_raw_none_is_unknown(self):
        assert Age.from_raw(None).is_unknown is True

    def test_negative_age_raises(self):
        with pytest.raises(ValueError):
            Age(value=-1.0)

    def test_age_over_120_raises(self):
        with pytest.raises(ValueError):
            Age(value=121.0)

    def test_is_minor_true_under_18(self):
        assert Age(value=17.9).is_minor is True

    def test_is_minor_false_at_18(self):
        assert Age(value=18.0).is_minor is False


class TestFamilyRelation:
    def test_total_family_size_includes_self(self):
        assert FamilyRelation(sib_sp=2, parch=3).total_family_size == 6  # 2+3+1

    def test_is_alone_when_both_zero(self):
        assert FamilyRelation(sib_sp=0, parch=0).is_alone is True

    def test_not_alone_with_siblings(self):
        assert FamilyRelation(sib_sp=1, parch=0).is_alone is False

    def test_is_large_family_at_5_or_more(self):
        assert FamilyRelation(sib_sp=2, parch=2).is_large_family is True  # 2+2+1=5

    def test_from_raw_parses_string_values(self):
        f = FamilyRelation.from_raw("1", "2")
        assert f.sib_sp == 1 and f.parch == 2

    def test_from_raw_none_defaults_to_zero(self):
        f = FamilyRelation.from_raw(None, None)
        assert f.sib_sp == 0 and f.parch == 0

    def test_negative_sib_sp_raises(self):
        with pytest.raises(ValueError):
            FamilyRelation(sib_sp=-1, parch=0)


class TestSurvived:
    def test_from_raw_1_means_survived(self):
        assert Survived.from_raw("1").is_survived is True

    def test_from_raw_0_means_not_survived(self):
        assert Survived.from_raw("0").is_survived is False

    def test_from_raw_none_is_unknown(self):
        assert Survived.from_raw(None).is_unknown is True

    def test_from_raw_invalid_raises(self):
        with pytest.raises(ValueError):
            Survived.from_raw("2")
