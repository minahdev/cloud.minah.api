"""마이페이지 코드 ↔ DB 라벨 변환 (최소 구현)."""

from __future__ import annotations

GENDER_LABELS: dict[str, str] = {
    "male": "남성",
    "female": "여성",
}

EXPERIENCE_LABELS: dict[str, str] = {}
FAVORITE_EXERCISE_LABELS: dict[str, str] = {}
WEEKLY_GOAL_LABELS: dict[str, str] = {}


def _to_code(value: str, labels: dict[str, str]) -> str:
    if value in labels:
        return value
    for code, label in labels.items():
        if label == value:
            return code
    return value


def _to_label(value: str, labels: dict[str, str]) -> str:
    return labels.get(value, value)


def gender_to_code(value: str) -> str:
    return _to_code(value, GENDER_LABELS)


def gender_to_label(value: str) -> str:
    return _to_label(value, GENDER_LABELS)


def experience_to_code(value: str) -> str:
    return _to_code(value, EXPERIENCE_LABELS)


def experience_to_label(value: str) -> str:
    return _to_label(value, EXPERIENCE_LABELS)


def favorite_exercise_to_code(value: str) -> str:
    return _to_code(value, FAVORITE_EXERCISE_LABELS)


def favorite_exercise_to_label(value: str) -> str:
    return _to_label(value, FAVORITE_EXERCISE_LABELS)


def weekly_goal_to_code(value: str) -> str:
    return _to_code(value, WEEKLY_GOAL_LABELS)


def weekly_goal_to_label(value: str) -> str:
    return _to_label(value, WEEKLY_GOAL_LABELS)
