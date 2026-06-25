from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooQuery, DunnCooResponse
from silicon_valley.app.ports.output.piper_dunn_coo_port import DunnCooPort


class DunnCooRepository(DunnCooPort):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: DunnCooQuery) -> DunnCooResponse:
        raise NotImplementedError
