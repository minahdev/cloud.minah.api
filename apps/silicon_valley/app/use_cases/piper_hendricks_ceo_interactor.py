from __future__ import annotations

from silicon_valley.adapter.inbound.api.schemas.piper_hendricks_ceo_schema import HendricksCeoSchema
from silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoQuery, HendricksCeoResponse
from silicon_valley.app.ports.input.piper_hendricks_ceo_use_case import HendricksCeoUseCase
from silicon_valley.app.ports.output.piper_hendricks_ceo_port import HendricksCeoPort


class HendricksCeoInteractor(HendricksCeoUseCase):

    def __init__(self, repository: HendricksCeoPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: HendricksCeoSchema) -> HendricksCeoResponse:
        return await self._repository.introduce_myself(HendricksCeoQuery(
            id=schema.id,
            name=schema.name,
        ))
