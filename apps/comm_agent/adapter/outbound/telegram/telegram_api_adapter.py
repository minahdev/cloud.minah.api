from __future__ import annotations

import logging
import os

import httpx

from comm_agent.app.ports.output.telegram_port import TelegramSenderPort

logger = logging.getLogger(__name__)


class TelegramApiAdapter(TelegramSenderPort):
    """Telegram Bot API(sendMessage)로 메시지 발송을 위임한다.

    .env 의 TELEGRAM_BOT_TOKEN 으로 봇 인증. chat_id 로 대상 지정.
    """

    def __init__(self) -> None:
        self._token = os.getenv("TELEGRAM_BOT_TOKEN", "")

    async def send(self, chat_id: str, text: str) -> dict:
        if not self._token:
            raise RuntimeError("'.env'에 TELEGRAM_BOT_TOKEN을 설정하세요.")

        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        logger.info("[TelegramApiAdapter] 발송 요청 | chat_id=%s", chat_id)

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json={"chat_id": chat_id, "text": text})
            data = response.json() if response.content else {}
            if not data.get("ok"):
                # 토큰 노출 방지: URL 대신 텔레그램이 준 description만 노출
                desc = data.get("description") or f"HTTP {response.status_code}"
                raise RuntimeError(f"텔레그램 발송 실패: {desc}")
            return data
