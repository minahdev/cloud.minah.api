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


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class TelegramSendQuery:

    id: int   # 직관적인 타입 변경
    name: str


@dataclass
class TelegramResponse:
    """텔레그램 자기소개 응답 (IntroduceResponse 대응)."""

    id: int
    name: str
    answer: str = ""