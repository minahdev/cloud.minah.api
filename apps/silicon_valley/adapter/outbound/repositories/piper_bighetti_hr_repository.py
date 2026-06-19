from __future__ import annotations

import logging
from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_bighetti_hr_dto import BighettiHrQuery, BighettiHrResponse
from silicon_valley.app.ports.output.piper_bighetti_hr_port import BighettiHrPort

logger = logging.getLogger(__name__)


class BighettiHrRepository(BighettiHrPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: BighettiHrQuery) -> BighettiHrResponse:
        logger.info("[BighettiHrRepository] introduce_myself | %s", query)
        return BighettiHrResponse(
            id=query.id,
            name=query.name + " — Big Head",
        )
