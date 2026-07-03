from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from vision.app.dtos.vision_dto import VisionIntroduceResponse, VisionQuery
from vision.app.ports.output.vision_port import VisionPort

logger = logging.getLogger(__name__)


class VisionRepository(VisionPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: VisionQuery) -> VisionIntroduceResponse:

        '''비전의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[VisionRepository] 🍗introduce_myself 진입 | request_data={query}")

        response = VisionIntroduceResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

        return response
