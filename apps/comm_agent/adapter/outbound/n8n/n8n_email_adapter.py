from __future__ import annotations

import logging
import os

import httpx

from comm_agent.app.ports.output.email_send_port import EmailSenderPort

logger = logging.getLogger(__name__)


class N8nEmailAdapter(EmailSenderPort):
    """n8n Webhook(→ Gmail) 으로 메일 발송을 위임한다.

    n8n 워크플로우: Webhook(POST) → Gmail(Send) → Respond to Webhook.
    webhook 으로 {to, subject, body} 를 보내면 Gmail 노드가 발송한다.
    """

    def __init__(self) -> None:
        self._webhook_url = os.getenv("N8N_EMAIL_WEBHOOK_URL", "")

    async def send(self, to: str, subject: str, body: str) -> dict:
        if not self._webhook_url:
            raise RuntimeError("'.env'에 N8N_EMAIL_WEBHOOK_URL을 설정하세요.")

        logger.info("[N8nEmailAdapter] 발송 요청 | to=%s | subject=%s", to, subject)

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self._webhook_url,
                json={"to": to, "subject": subject, "body": body},
            )
            response.raise_for_status()
            return response.json() if response.content else {}
