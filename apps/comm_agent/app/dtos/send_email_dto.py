from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SendEmailCommand:
    """유스케이스 입력 — 받는 사람 + 본문 주제."""

    to: str
    topic: str


@dataclass
class SendEmailResponse:
    """발송 결과."""

    success: bool
    to: str
    subject: str
    message: str = "메일을 발송했습니다."
