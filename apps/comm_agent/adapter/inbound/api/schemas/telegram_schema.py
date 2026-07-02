from __future__ import annotations

from pydantic import BaseModel, Field


class TelegramSendSchema(BaseModel):
    """프론트 → POST /comm_agent/telegram/send 요청.

    chat_id: 받는 텔레그램 채팅 ID(또는 @사용자명), topic: 메시지 주제.
    """

    chat_id: str = Field(..., min_length=1, max_length=100, description="텔레그램 chat_id 또는 @username")
    topic: str = Field(..., min_length=1, max_length=500, description="메시지 주제")

    model_config = {
        "json_schema_extra": {
            "example": {
                "chat_id": "123456789",
                "topic": "내일 모임 시간 변경 안내",
            }
        }
    }


class TelegramIntroduceSchema(BaseModel):
    """Telegram Agent 자기소개 입력."""

    id: int
    name: str
