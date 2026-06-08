from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

GenderCode = Literal["male", "female"]


class MyPageProfileSchema(BaseModel):
    """마이페이지 프로필 — secom_users 확장 컬럼."""

    model_config = ConfigDict(populate_by_name=True)

    userId: str = Field(..., min_length=1, max_length=64)
    name: str = Field(..., min_length=1, max_length=64)
    gender: GenderCode
    birthDate: str = Field(..., min_length=8, max_length=8)
    phone: str = Field(..., min_length=1, max_length=32)
    heightCm: float = Field(..., gt=0, le=300)
    weightKg: float = Field(..., gt=0, le=500)
    favoriteExercise: str = Field(..., max_length=32)
    favoriteExerciseOther: str = Field(default="", max_length=128)
    experience: str = Field(..., max_length=32)
    weeklyGoal: str = Field(..., max_length=32)
    healthNote: str = Field(default="", max_length=2000)


class MyPageProfileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    userId: str
    name: str | None = None
    gender: GenderCode | None = None
    genderLabel: str | None = None
    birthDate: str | None = None
    phone: str | None = None
    heightCm: float | None = None
    weightKg: float | None = None
    favoriteExercise: str | None = None
    favoriteExerciseOther: str | None = None
    experience: str | None = None
    weeklyGoal: str | None = None
    experienceLabel: str | None = None
    weeklyGoalLabel: str | None = None
    favoriteExerciseLabel: str | None = None
    healthNote: str | None = None
    message: str = "ok"
