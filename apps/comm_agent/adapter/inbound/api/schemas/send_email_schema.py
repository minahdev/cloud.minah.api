from __future__ import annotations

from pydantic import BaseModel, Field


class SendEmailSchema(BaseModel):
    """프론트 → POST /comm_agent/send 요청.

    email: 받는 사람 주소, topic: 본문을 생성할 주제.
    """

    email: str = Field(
        ...,
        min_length=3,
        max_length=254,
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        description="받는 사람 이메일",
    )
    topic: str = Field(..., min_length=1, max_length=500, description="이메일 본문 주제")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "someone@example.com",
                "topic": "다음 주 팀 회식 안내",
            }
        }
    }


class ComposeEmailIntroduceSchema(BaseModel):
    """Comm Agent 자기소개 입력."""

    id: int
    name: str
