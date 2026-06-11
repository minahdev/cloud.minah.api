from __future__ import annotations

from fastapi import Depends

from minahai.apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from minahai.apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from minahai.apps.titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer
from minahai.apps.titanic.dependencies.passenger_rose_model_provider import get_rose_model
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    SmithCaptainSchema,
    ChatSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainQuery
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

import logging

logger = logging.getLogger(__name__)

class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository) -> None:
        self._repository = repository



    async def chat(self, schema: ChatSchema,
                rose: RoseModelUseCase = Depends(get_rose_model),
                jack: JackTrainerUseCase = Depends(get_jack_trainer)
                   
                   
                   ) -> SmithCaptainResponse:
        
        
        
        return await self._repository.chat(schema.message)


    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        #스미스 선장의 자기소개 인터랙트

        return await self._repository.introduce_myself(SmithCaptainQuery(
            id= schema.id,
            name= schema.name
        ))

    