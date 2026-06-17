from __future__ import annotations

from typing import Any

from kiwipiepy import Kiwi
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from titanic.app.ports.output.crew_andrews_architect_port import AndrewsArchitectPort

import logging

logger = logging.getLogger(__name__)

_INTENT_KEYWORDS: dict[str, list[str]] = {
    "SURVIVAL_QUERY":  ["살았", "생존", "살아남", "survived", "survival"],
    "ACCURACY_QUERY":  ["정확도", "accuracy", "성능", "얼마나"],
    "ALGORITHM_QUERY": ["알고리즘", "모델", "방법", "어떤"],
    "RANKING_QUERY":   ["순위", "랭킹", "1위", "최고"],
}

class AndrewsArchitectRepository(AndrewsArchitectPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._kiwi = Kiwi()

    def analyze_intent(self, question: str) -> dict[str, Any]:
        tokens = self._kiwi.tokenize(question)
        morphs = [t.form for t in tokens]
        text_lower = question.lower()

        for intent, keywords in _INTENT_KEYWORDS.items():
            if any(kw in text_lower or kw in morphs for kw in keywords):
                return {"intent": intent, "morphs": morphs}
        return {"intent": "UNKNOWN", "morphs": morphs}

    def introduce_myself(self, query: AndrewsArchitectQuery) -> AndrewsArchitectResponse:

        '''앤드류의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[AndrewsArchitectPgRepository] 🍕introduce_myself 진입 | request_data={query}")

        response: AndrewsArchitectResponse = AndrewsArchitectResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )

        return response