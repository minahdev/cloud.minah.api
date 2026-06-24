import os

from silicon_valley.adapter.outbound.client.n8n_client import N8nClient

N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "https://your-n8n-instance.com/webhook/...")


def get_n8n_client() -> N8nClient:
    return N8nClient(webhook_url=N8N_WEBHOOK_URL)
