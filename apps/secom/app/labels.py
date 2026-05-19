"""마이페이지 코드 ↔ 한글 라벨 (DB에는 한글 저장, API는 코드 반환)."""

EXPERIENCE_LABELS: dict[str, str] = {
    "under_1": "1년 미만",
    "1_to_2": "1년 이상 ~ 2년 미만",
    "2_to_3": "2년 이상 ~ 3년 미만",
    "3_to_5": "3년 이상 ~ 5년 미만",
    "over_5": "5년 이상",
}

WEEKLY_GOAL_LABELS: dict[str, str] = {
    "1_2": "주 1~2회",
    "3_4": "주 3~4회",
    "5_plus": "주 5회 이상",
}

FAVORITE_EXERCISE_LABELS: dict[str, str] = {
    "gym": "헬스",
    "running": "러닝",
    "cycling": "자전거",
    "other": "기타",
}

_EXPERIENCE_CODE_BY_LABEL = {v: k for k, v in EXPERIENCE_LABELS.items()}
_WEEKLY_GOAL_CODE_BY_LABEL = {v: k for k, v in WEEKLY_GOAL_LABELS.items()}
_FAVORITE_EXERCISE_CODE_BY_LABEL = {v: k for k, v in FAVORITE_EXERCISE_LABELS.items()}


def experience_to_label(code: str) -> str:
    return EXPERIENCE_LABELS.get(code, code)


def experience_to_code(stored: str | None) -> str | None:
    if stored is None:
        return None
    if stored in EXPERIENCE_LABELS:
        return stored
    return _EXPERIENCE_CODE_BY_LABEL.get(stored, stored)


def weekly_goal_to_label(code: str) -> str:
    return WEEKLY_GOAL_LABELS.get(code, code)


def weekly_goal_to_code(stored: str | None) -> str | None:
    if stored is None:
        return None
    if stored in WEEKLY_GOAL_LABELS:
        return stored
    return _WEEKLY_GOAL_CODE_BY_LABEL.get(stored, stored)


def favorite_exercise_to_label(code: str) -> str:
    return FAVORITE_EXERCISE_LABELS.get(code, code)


def favorite_exercise_to_code(stored: str | None) -> str | None:
    if stored is None:
        return None
    if stored in FAVORITE_EXERCISE_LABELS:
        return stored
    return _FAVORITE_EXERCISE_CODE_BY_LABEL.get(stored, stored)
