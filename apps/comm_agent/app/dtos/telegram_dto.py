from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TelegramSendCommand:
    """유스케이스 입력 — 받는 채팅(chat_id) + 메시지 주제."""

    chat_id: str
    topic: str


@dataclass
class TelegramSendResponse:
    """발송 결과."""

    success: bool
    chat_id: str
    message: str = "텔레그램 메시지를 발송했습니다."
