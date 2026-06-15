from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FoodSearchQuery:
    keyword: str


@dataclass(frozen=True)
class FoodCreateCommand:
    name: str
    calories_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float
    serving_size: float
    serving_unit: str
    created_by: str


@dataclass(frozen=True)
class FoodDto:
    id: int
    name: str
    calories_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float
    serving_size: float
    serving_unit: str
    created_by: str | None
