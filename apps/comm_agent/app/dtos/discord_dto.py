from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DiscordResponse:
    """디스코드 자기소개 응답 (IntroduceResponse 대응)."""

    id: int
    name: str
    answer: str = ""


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class DiscordQuery:
    
    id: int   # 직관적인 타입 변경
    name: str