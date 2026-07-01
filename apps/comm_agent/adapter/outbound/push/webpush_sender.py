from __future__ import annotations

import asyncio
import logging
import os

from pywebpush import WebPushException, webpush

from comm_agent.app.dtos.push_dto import PushSubscriptionInfo
from comm_agent.app.ports.output.push_sender_port import PushSenderPort

logger = logging.getLogger(__name__)


class WebPushSender(PushSenderPort):
    """pywebpush(VAPID)로 브라우저 푸시 서비스에 메시지를 발송한다."""

    def __init__(self) -> None:
        self._private_key = os.getenv("VAPID_PRIVATE_KEY", "")
        self._subject = os.getenv("VAPID_SUBJECT", "mailto:admin@example.com")

    def _send_sync(self, subscription: PushSubscriptionInfo, payload: str) -> bool:
        try:
            webpush(
                subscription_info={
                    "endpoint": subscription.endpoint,
                    "keys": {"p256dh": subscription.p256dh, "auth": subscription.auth},
                },
                data=payload,
                vapid_private_key=self._private_key,
                vapid_claims={"sub": self._subject},
            )
            return True
        except WebPushException as e:
            status = getattr(e.response, "status_code", None)
            # 404/410 = 만료된 구독. 그 외도 이번 발송은 실패.
            logger.warning("[WebPushSender] 발송 실패 status=%s | %s", status, e)
            return False

    async def send(self, subscription: PushSubscriptionInfo, payload: str) -> bool:
        if not self._private_key:
            raise RuntimeError("'.env'에 VAPID_PRIVATE_KEY를 설정하세요.")
        # pywebpush는 동기(blocking) → 스레드로 넘겨 이벤트 루프 안 막음
        return await asyncio.to_thread(self._send_sync, subscription, payload)
