from __future__ import annotations

from fastapi import APIRouter

from comm_agent.adapter.inbound.api.v1.contact_router import (
    contact_router as _contact_v1_router,
)
from comm_agent.adapter.inbound.api.v1.discord_router import (
    discord_router as _discord_v1_router,
)
from comm_agent.adapter.inbound.api.v1.email_send_router import (
    comm_agent_router as _comm_agent_v1_router,
)
from comm_agent.adapter.inbound.api.v1.judge_router import (
    judge_router as _judge_v1_router,
)
from comm_agent.adapter.inbound.api.v1.monitor_watcher_router import (
    monitor_watcher_router as _monitor_v1_router,
)
from comm_agent.adapter.inbound.api.v1.push_subscription_router import (
    push_router as _push_v1_router,
)
from comm_agent.adapter.inbound.api.v1.received_mail_router import (
    receive_router as _receive_v1_router,
)
from comm_agent.adapter.inbound.api.v1.telegram_router import (
    telegram_router as _telegram_v1_router,
)

comm_agent_router = APIRouter()
comm_agent_router.include_router(_comm_agent_v1_router)
comm_agent_router.include_router(_contact_v1_router)
comm_agent_router.include_router(_discord_v1_router)
comm_agent_router.include_router(_judge_v1_router)
comm_agent_router.include_router(_monitor_v1_router)
comm_agent_router.include_router(_push_v1_router)
comm_agent_router.include_router(_receive_v1_router)
comm_agent_router.include_router(_telegram_v1_router)

__all__ = ["comm_agent_router"]
