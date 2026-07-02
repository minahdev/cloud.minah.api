from __future__ import annotations

from dataclasses import dataclass


@dataclass
class JudgeResponse:
    """심판(Judge) 자기소개 응답 (IntroduceResponse 대응)."""

    id: int
    name: str
    answer: str = ""
