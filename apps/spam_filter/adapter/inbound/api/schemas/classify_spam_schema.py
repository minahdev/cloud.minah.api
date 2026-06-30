from __future__ import annotations

from pydantic import BaseModel, Field


class ClassifySpamSchema(BaseModel):
    """프론트 → POST /spam_filter/classify 요청.

    subject: 메일 제목, body: 메일 본문.
    """

    subject: str = Field(..., min_length=1, max_length=500, description="메일 제목")
    body: str = Field(..., min_length=1, max_length=10000, description="메일 본문")

    model_config = {
        "json_schema_extra": {
            "example": {
                "subject": "[보안 경고] 계정 정지 안내",
                "body": "본인 인증을 위해 비밀번호 확인이 필요합니다.",
            }
        }
    }
