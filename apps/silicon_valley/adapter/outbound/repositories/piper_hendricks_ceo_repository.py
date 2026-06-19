from __future__ import annotations

import logging
from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoQuery, HendricksCeoResponse
from silicon_valley.app.ports.output.piper_hendricks_ceo_port import HendricksCeoPort

logger = logging.getLogger(__name__)


class HendricksCeoRepository(HendricksCeoPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: HendricksCeoQuery) -> HendricksCeoResponse:
        logger.info("[HendricksCeoRepository] introduce_myself | %s", query)
        return HendricksCeoResponse(
            id=query.id,
            name=query.name + " — Pied Piper CEO",
        )
