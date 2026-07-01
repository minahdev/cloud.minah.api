from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PushSubscriptionCommand:
    """웹 푸시 구독 저장 입력 1건."""

    endpoint: str
    p256dh: str
    auth: str


@dataclass
class PushSubscriptionInfo:
    """푸시 발송에 필요한 구독 정보 1건."""

    endpoint: str
    p256dh: str
    auth: str
