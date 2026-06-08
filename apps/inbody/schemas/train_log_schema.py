from pydantic import BaseModel, Field


class TrainDailyLogPayload(BaseModel):
    userId: str = Field(min_length=1)
    date: str
    muscles: list[str] = Field(default_factory=list)
    workout: str = ""
    weightKg: float | None = None
    diet: dict = Field(default_factory=dict)
    memo: str = ""
    exerciseMinutes: int | None = None


class TrainDailyLogResponse(BaseModel):
    date: str
    muscles: list[str] = Field(default_factory=list)
    workout: str = ""
    weightKg: float | None = None
    diet: dict = Field(default_factory=dict)
    memo: str = ""
    exerciseMinutes: int | None = None
    updatedAt: str
