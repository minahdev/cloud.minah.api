from __future__ import annotations

from silicon_valley.adapter.inbound.api.schemas.piper_gilfoyle_sys_schema import GilfoyleSysSchema
from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import GilfoyleSysQuery, GilfoyleSysResponse
from silicon_valley.app.ports.input.piper_gilfoyle_sys_use_case import GilfoyleSysUseCase
from silicon_valley.app.ports.output.piper_gilfoyle_sys_port import GilfoyleSysPort


class GilfoyleSysInteractor(GilfoyleSysUseCase):

    def __init__(self, repository: GilfoyleSysPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: GilfoyleSysSchema) -> GilfoyleSysResponse:
        return await self._repository.introduce_myself(GilfoyleSysQuery(
            id=schema.id,
            name=schema.name,
        ))
