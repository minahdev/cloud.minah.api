from __future__ import annotations

from pydantic import BaseModel, Field


class ReceiveMailSchema(BaseModel):
    """n8n → POST /comm_agent/receive/gmail 요청.

    n8n이 Gmail(IMAP/Gmail Trigger)에서 감지한 새 메일을 전달한다.
    n8n 노드마다 필드명이 달라질 수 있어 추가 필드는 허용(extra=allow)한다.
    """

    from_: str = Field(..., alias="from", description="보낸 사람 주소")
    subject: str = Field(default="", max_length=1000, description="메일 제목")
    body: str = Field(default="", description="메일 본문")

    model_config = {
        "populate_by_name": True,
        "extra": "allow",
        "json_schema_extra": {
            "example": {
                "from": "someone@example.com",
                "subject": "문의드립니다",
                "body": "안녕하세요, 문의 내용입니다.",
            }
        },
    }


class ReceivedMailViewSchema(BaseModel):
    """GET /comm_agent/receive 응답 — 저장된 수신 메일 1건."""

    id: int
    sender: str
    subject: str
    body: str
    received_at: str


class ReceivedMailIntroduceSchema(BaseModel):
    """수신 메일(Received Mail) 자기소개 입력."""

    id: int
    name: str
