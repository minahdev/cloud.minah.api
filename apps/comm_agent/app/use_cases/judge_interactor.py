from __future__ import annotations

import logging

from comm_agent.adapter.inbound.api.schemas.judge_schema import (
    JudgeSchema,
)
from comm_agent.app.dtos.judge_dto import JudgeResponse
from comm_agent.app.ports.input.judge_use_case import JudgeUseCase

logger = logging.getLogger(__name__)


class JudgeInteractor(JudgeUseCase):
    async def introduce_myself(self, schema: JudgeSchema) -> JudgeResponse:
        logger.info("[Judge] introduce_myself | id=%s name=%s", schema.id, schema.name)
        return JudgeResponse(
            id=schema.id,
            name=schema.name,
            answer=(
                f"안녕하세요, 저는 '{schema.name}'입니다. "
                "규칙에 따라 옳고 그름과 통과 여부를 판정합니다."
            ),
        )
