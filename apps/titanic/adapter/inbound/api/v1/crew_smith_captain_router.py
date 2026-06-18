from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends

from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_crew_smith_captain_use_case
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema, ChatSchema


logger = logging.getLogger(__name__)

crew_smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])



@crew_smith_captain_router.post("/chat", response_model=SmithCaptainResponse)
async def chat(
    schema: Annotated[ChatSchema,Body()],
    smith: SmithCaptainUseCase = Depends(get_crew_smith_captain_use_case)

) -> SmithCaptainResponse:
    


    # minahview(프론트엔드)에서 smith/page.tsx 에서 /api/titanic/smith/chat 이 url 로
    # 키 값이 messages 인 Body()로 보낸 내용을 로그로 출력하는 코드
    logger.info("[스미스 선장] 사용자 질문: %s", schema.messages)
    question: str = schema.messages[-1]["content"]
    return await smith.chat(question)
    
    




@crew_smith_captain_router.get("/myself", response_model=SmithCaptainResponse)
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_crew_smith_captain_use_case))-> SmithCaptainResponse:
    
    return await smith.introduce_myself(
        SmithCaptainSchema(
            id=5,
            name="Edward John Smith",
        )
    )



    