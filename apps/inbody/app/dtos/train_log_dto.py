from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TrainLogSaveCommand:
    user_id: str
    date: str
    muscles: list[str] = field(default_factory=list)
    workout: str = ""
    weight_kg: float | None = None
    diet: dict = field(default_factory=dict)
    memo: str = ""
    exercise_minutes: int | None = None


@dataclass
class TrainLogDto:
    date: str
    updated_at: str
    muscles: list[str] = field(default_factory=list)
    workout: str = ""
    weight_kg: float | None = None
    diet: dict = field(default_factory=dict)
    memo: str = ""
    exercise_minutes: int | None = None
