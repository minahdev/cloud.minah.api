from __future__ import annotations

from pydantic import BaseModel, Field

from star_craft.domain.ontology.communication.email_type import EmailType


class ComposeEmailSchema(BaseModel):
    """프론트 → POST /star_craft/compose-email 요청.

    email: 받는 사람, topic: 본문 주제, email_type: 작성 유형(온톨로지 규격 선택).
    """

    email: str = Field(
        ...,
        min_length=3,
        max_length=254,
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        description="받는 사람 이메일",
    )
    subject: str = Field("", max_length=200, description="메일 제목 (비우면 주제로 대체)")
    sender_name: str = Field("", max_length=100, description="보내는 사람 이름 (서명에 사용)")
    topic: str = Field(..., min_length=1, max_length=500, description="이메일 본문 주제")
    email_type: EmailType = Field(EmailType.GENERAL, description="작성 유형(온톨로지 규격)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "someone@example.com",
                "subject": "팀 회식 안내드립니다",
                "topic": "다음 주 팀 회식 안내",
                "email_type": "meeting",
            }
        }
    }
