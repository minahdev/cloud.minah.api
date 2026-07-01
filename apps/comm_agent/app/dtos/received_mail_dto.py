from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReceivedMailCommand:
    """수신 메일 저장 입력 1건."""

    sender: str
    subject: str
    body: str


@dataclass
class ReceivedMailView:
    """수신 메일 조회 결과 1건."""

    id: int
    sender: str
    subject: str
    body: str
    received_at: str
