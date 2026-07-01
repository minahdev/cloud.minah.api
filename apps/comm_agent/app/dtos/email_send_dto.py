from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SendEmailCommand:
    """유스케이스 입력 — 받는 사람 + 본문 주제 + (Hub 온톨로지가 정한) 작성 규격.

    규격 필드(type_label·tone·required_elements)는 star_craft 온톨로지가 채워 넘긴다.
    비어 있으면 일반 메일로 작성한다.
    """

    to: str
    topic: str
    subject: str = ""  # 메일 제목 (비어 있으면 topic으로 폴백)
    sender_name: str = ""  # 보내는 사람 이름 (서명에 사용)
    type_label: str = ""
    tone: str = ""
    required_elements: tuple[str, ...] = ()


@dataclass
class SendEmailResponse:
    """발송 결과."""

    success: bool
    to: str
    subject: str
    message: str = "메일을 발송했습니다."


@dataclass
class IntroduceResponse:
    """introduce_myself 응답 (titanic JamesIntroduceResponse 대응)."""

    id: int
    name: str
    answer: str = ""
