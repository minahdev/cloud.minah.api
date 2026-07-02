from __future__ import annotations

from pydantic import BaseModel, Field


class VapidPublicKeyResponse(BaseModel):
    """GET /comm_agent/push/vapid-public-key 응답."""

    public_key: str


class PushKeysSchema(BaseModel):
    """브라우저 PushSubscription.keys."""

    p256dh: str
    auth: str


class PushSubscribeSchema(BaseModel):
    """POST /comm_agent/push/subscribe 요청 — 브라우저 구독 객체."""

    endpoint: str = Field(..., description="푸시 서비스 endpoint URL")
    keys: PushKeysSchema


class PushIntroduceSchema(BaseModel):
    """웹 푸시(Push) 자기소개 입력."""

    id: int
    name: str
