from __future__ import annotations

from pydantic import BaseModel, Field


class FoodCreateRequest(BaseModel):
    userId: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=200)
    caloriesKcal: float = Field(ge=0)
    proteinG: float = Field(ge=0, default=0.0)
    carbsG: float = Field(ge=0, default=0.0)
    fatG: float = Field(ge=0, default=0.0)
    servingSize: float = Field(gt=0, default=100.0)
    servingUnit: str = Field(default="g", max_length=20)


class FoodResponse(BaseModel):
    id: int
    name: str
    caloriesKcal: float
    proteinG: float
    carbsG: float
    fatG: float
    servingSize: float
    servingUnit: str
    createdBy: str | None
