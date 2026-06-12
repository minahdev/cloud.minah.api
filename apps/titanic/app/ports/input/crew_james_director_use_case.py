from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from titanic.adapter.inbound.api.schemas.crew_james_director_schema import TitanicRecordSchema, JamesDirectorSchema

from titanic.app.dtos.crew_james_director_dto import JamesIntroduceResponse


class JamesDirectorUseCase(ABC):

    @abstractmethod
    async def upload_titanic_file(self, schema: list[TitanicRecordSchema]):
        pass

    @abstractmethod
    async def introduce_myself(self, schema: JamesDirectorSchema) -> JamesIntroduceResponse:
        pass
