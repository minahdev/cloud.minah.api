from __future__ import annotations

import logging
import os

import httpx

from comm_agent.app.ports.output.telegram_port import TelegramSenderPort

logger = logging.getLogger(__name__)


class N8nTelegramAdapter(TelegramSenderPort):
    """n8n Webhook(→ Telegram) 으로 메시지 발송을 위임한다.

    n8n 워크플로우: Webhook(POST) → Telegram(sendMessage) → Respond to Webhook.
    webhook 으로 {chat_id, text} 를 보내면 Telegram 노드가 발송한다.
    (이메일의 N8nEmailAdapter와 동일 패턴)
    """

    def __init__(self) -> None:
        self._webhook_url = os.getenv("N8N_TELEGRAM_WEBHOOK_URL", "")

    async def send(self, chat_id: str, text: str) -> dict:
        if not self._webhook_url:
            raise RuntimeError("'.env'에 N8N_TELEGRAM_WEBHOOK_URL을 설정하세요.")

        logger.info("[N8nTelegramAdapter] 발송 요청 | chat_id=%s", chat_id)

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self._webhook_url,
                json={"chat_id": chat_id, "text": text},
            )
            response.raise_for_status()
            return response.json() if response.content else {}
