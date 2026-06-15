from __future__ import annotations

from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import (
    JackTrainerSchema
)
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse, JackTrainerQuery
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

import logging

logger = logging.getLogger(__name__)

class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository) -> None:
        self._repository = repository
        self._kiwi = Kiwi()


    async def analyze_message_intent(self, user_message: str) -> dict:
        #사용자의 질문(message)을 형태소 분석하여 키워드와 의도를 파악한다.
        tokens = self._kiwi.tokenize(user_message)

        keywords = [t.form for t in tokens if t.tag in ("NNG", "NNP", "SL")]
        verbs    = [t.form for t in tokens if t.tag.startswith("V")]

        logger.info("[JackTrainer] 형태소 분석 | message=%s | keywords=%s | verbs=%s", user_message, keywords, verbs)

        return {
            "keywords": keywords,
            "verbs":    verbs,
            "tokens":   [(t.form, t.tag) for t in tokens],
        }

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        
        return await self._repository.introduce_myself(JackTrainerQuery(
            id= schema.id,
            name= schema.name
        ))