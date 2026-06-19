from __future__ import annotations

from silicon_valley.adapter.inbound.api.schemas.piper_bighetti_hr_schema import BighettiHrSchema
from silicon_valley.app.dtos.piper_bighetti_hr_dto import BighettiHrQuery, BighettiHrResponse
from silicon_valley.app.ports.input.piper_bighetti_hr_use_case import BighettiHrUseCase
from silicon_valley.app.ports.output.piper_bighetti_hr_port import BighettiHrPort


class BighettiHrInteractor(BighettiHrUseCase):

    def __init__(self, repository: BighettiHrPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: BighettiHrSchema) -> BighettiHrResponse:
        return await self._repository.introduce_myself(BighettiHrQuery(
            id=schema.id,
            name=schema.name,
        ))
