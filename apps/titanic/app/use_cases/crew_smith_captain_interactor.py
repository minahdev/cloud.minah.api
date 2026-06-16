from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    SmithCaptainSchema,
    ChatSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainQuery, SmithCaptainChatCommand
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

import logging

logger = logging.getLogger(__name__)

class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
            self, 
            repository: SmithCaptainRepository,
            rose: RoseModelUseCase,
            jack: JackTrainerUseCase,
            cal: CalTesterUseCase,
            walter: WalterRoasterUseCase
        ):
        
        self._repository = repository
        self.rose = rose
        self.jack = jack
        self.cal = cal
        self.walter = walter
        
        

    async def chat(self, schema: ChatSchema) -> SmithCaptainResponse:
        #schema에 들어있는 messages 내용 보기
        logger.info(f"[SmithCaptainInteractor] chat 진입 | messages = {schema.messages}")
        train_set = self.walter.get_train_set()
        test_set = self.walter.get_test_set()
        self.jack.train_model(train_set)
        self.cal.test_model(test_set)
        


        return SmithCaptainResponse(text="1309명입니다.")


    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        #스미스 선장의 자기소개 인터랙트

        return await self._repository.introduce_myself(SmithCaptainQuery(
            id= schema.id,
            name= schema.name
        ))

    