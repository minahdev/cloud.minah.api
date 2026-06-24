import httpx
from typing import Dict, Any


class N8nClient:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send_event(self, payload: Dict[str, Any]) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.webhook_url, json=payload)
                return response.status_code == 200
            except Exception as e:
                print(f"n8n 전송 실패: {e}")
                return False
