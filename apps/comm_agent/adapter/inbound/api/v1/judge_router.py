from fastapi import APIRouter, Depends

from comm_agent.adapter.inbound.api.schemas.judge_schema import JudgeSchema
from comm_agent.app.dtos.judge_dto import JudgeResponse
from comm_agent.app.ports.input.judge_use_case import JudgeUseCase
from comm_agent.dependencies.judge_provider import get_judge_use_case

"""
심판 (Judge)
역할 (keyword): judge (판정/심사)
규칙에 따라 옳고 그름·통과 여부를 판정하는 심사자.
"""

judge_router = APIRouter(prefix="/comm_agent/judge", tags=["comm_agent_judge"])


@judge_router.get("/myself", response_model=JudgeResponse)
async def introduce_myself(
    judge: JudgeUseCase = Depends(get_judge_use_case),
) -> JudgeResponse:
    return await judge.introduce_myself(
        JudgeSchema(
            id=4,
            name="심판 (Judge)",
        )
    )
