from __future__ import annotations
from typing import Any

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainQuery
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort

import logging

logger = logging.getLogger(__name__)


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
        self,
        repository: Any,
        rose: RoseModelUseCase,
        jack: JackTrainerUseCase,
        cal: CalTesterUseCase,
        walter: WalterRoasterUseCase,
        andrews: AndrewsArchitectUseCase,
        lowe: LoweBoatUseCase,
        hartley: HartleyViolinUseCase,
    ):
        self._repository = repository
        self.rose = rose
        self.jack = jack
        self.cal = cal
        self.walter = walter
        self.andrews = andrews
        self.lowe = lowe
        self.hartley = hartley

    async def chat(self, question: str) -> SmithCaptainResponse:
        train_set: pd.DataFrame = await self.walter.get_train_set()
        X_train, y_label = self.lowe.feature_engineering(train_set)
        train_result = await self.jack.train_model(X_train, y_label)
        cal_result = await self.cal.test_model({"df": train_set, "trained_strategies": train_result["trained_strategies"]})
        champion = train_result["trained_strategies"][cal_result["champion"]["key"]]
        answer: str = self.andrews.answer(question, train_set, champion)
        return SmithCaptainResponse(text=answer)
    

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        return self._repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))
