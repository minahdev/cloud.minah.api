from __future__ import annotations

from dataclasses import dataclass

from star_craft.domain.ontology.spam.spam_category import SpamCategory


@dataclass
class ClassifySpamCommand:
    """유스케이스 입력 — 분류할 메일의 제목 + 본문."""

    subject: str
    body: str


@dataclass
class ClassifySpamResponse:
    """분류 결과 — 카테고리 + 매칭된 신호."""

    category: SpamCategory
    is_spam: bool
    matched_keywords: list[str]
