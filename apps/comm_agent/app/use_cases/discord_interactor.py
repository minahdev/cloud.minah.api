from __future__ import annotations

import logging

from comm_agent.adapter.inbound.api.schemas.discord_schema import (
    DiscordIntroduceSchema,
)
from comm_agent.app.dtos.discord_dto import DiscordQuery, DiscordResponse
from comm_agent.app.ports.input.discord_use_case import DiscordUseCase
from comm_agent.app.ports.output.discord_port import DiscordPort

logger = logging.getLogger(__name__)


class DiscordInteractor(DiscordUseCase):
    def __init__(self, repository: DiscordPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: DiscordIntroduceSchema) -> DiscordResponse:
        
        return await self._repository.introduce_myself(DiscordQuery(
            id= schema.id,
            name= schema.name
        ))
