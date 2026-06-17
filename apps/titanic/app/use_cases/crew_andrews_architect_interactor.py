from __future__ import annotations
from typing import Any

from kiwipiepy import Kiwi



from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import (
    AndrewsArchitectSchema,
)
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse, AndrewsArchitectQuery
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_port import AndrewsArchitectPort

import logging

logger = logging.getLogger(__name__)

INTENT_MAP: dict[str, set[str]] = {
    "SURVIVAL_PREDICT": {"살았", "생존", "살아남", "죽었", "사망", "예측", "확률", "survived"},
    "STATISTICS":       {"몇", "수", "명", "총", "전체", "인원", "통계", "비율"},
    "PASSENGER_SEARCH": {"누구", "이름", "승객", "탑승", "찾", "검색"},
    "MODEL_TRAIN":      {"학습", "훈련", "모델", "알고리즘", "정확도", "성능"},
}

class AndrewsArchitectInteractor(AndrewsArchitectUseCase):

    def __init__(self, repository: AndrewsArchitectPort):
        self.repository = repository
        self.kiwi = Kiwi()

    def analyze_intent(self, messages: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 프론트 질문의 의도를 파악하는 메소드

        반환값:
            intent   : 감지된 의도 (SURVIVAL_PREDICT / STATISTICS / PASSENGER_SEARCH / MODEL_TRAIN / UNKNOWN)
            keywords : 분석에 사용된 핵심 형태소 목록
            scores   : 의도별 매칭 점수
            tokens   : Kiwi가 분석한 전체 (형태소, 품사) 쌍 목록
        '''
        # 명사(NN*), 동사 어간(VV/VA), 파생어근(XR)만 의도 판별에 사용
        tokens = self.kiwi.tokenize(messages)
        keywords = [t.form for t in tokens if t.tag.startswith(("NN", "VV", "VA", "XR"))]

        scores: dict[str, int] = {intent: 0 for intent in INTENT_MAP}
        for keyword in keywords:
            for intent, kw_set in INTENT_MAP.items():
                if keyword in kw_set:
                    scores[intent] += 1

        best_intent = max(scores, key=lambda k: scores[k])
        intent = best_intent if scores[best_intent] > 0 else "UNKNOWN"

        logger.info(
            f"[AndrewsArchitectInteractor] analyze_intent | messages={messages!r} "
            f"intent={intent} scores={scores}"
        )
        return {
            "intent": intent,
            "keywords": keywords,
            "scores": scores,
            "tokens": [(t.form, str(t.tag)) for t in tokens],
        }

    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        '''앤드류 설계자의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(AndrewsArchitectQuery(
            id = schema.id,
            name = schema.name
        ))
