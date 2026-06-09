from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LessonSaveCommand:
    user_id: str
    client_id: str
    date: str
    title: str
    time: str
    schedule_note: str
    member_user_id: str | None = None
    record: dict | None = None
    created_at: str | None = None


@dataclass
class LessonListQuery:
    user_id: str
    member_user_id: str | None = None


@dataclass
class LessonDeleteCommand:
    user_id: str
    client_id: str
    member_user_id: str | None = None


@dataclass
class LessonDto:
    id: str
    date: str
    title: str
    time: str
    schedule_note: str
    created_at: str
    member_user_id: str
    record: dict | None = None
