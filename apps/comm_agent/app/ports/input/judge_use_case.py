from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from comm_agent.app.dtos.judge_dto import JudgeResponse

if TYPE_CHECKING:
    from comm_agent.adapter.inbound.api.schemas.judge_schema import (
        JudgeSchema,
    )


class JudgeUseCase(ABC):
    """심판(Judge) — 규칙에 따라 옳고 그름·통과 여부를 판정하는 심사자."""

    @abstractmethod
    async def introduce_myself(self, schema: JudgeSchema) -> JudgeResponse:
        pass
