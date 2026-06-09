from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TodayStorySaveCommand:
    user_id: str
    date: str | None
    mood: str | None
    story: str


@dataclass
class TodayStoryDto:
    date: str
    mood: str | None
    story: str
    updated_at: str
