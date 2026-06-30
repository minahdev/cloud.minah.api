from __future__ import annotations

import logging

from star_craft.domain.ontology.spam.spam_category import SpamCategory
from star_craft.domain.ontology.spam.spam_taxonomy import SPAM_TAXONOMY

from spam_filter.app.dtos.classify_spam_dto import ClassifySpamCommand, ClassifySpamResponse
from spam_filter.app.ports.input.classify_spam_use_case import ClassifySpamUseCase

logger = logging.getLogger(__name__)


class ClassifySpamInteractor(ClassifySpamUseCase):
    """star_craft 스팸 온톨로지를 읽어 메일을 분류한다.

    온톨로지(개념·키워드)는 Hub 소유, 판정 로직은 여기(스포크) 소유.
    가장 많은 키워드가 매칭된 개념으로 분류하고, 매칭이 없으면 HAM.
    """

    def classify(self, command: ClassifySpamCommand) -> ClassifySpamResponse:
        text = f"{command.subject} {command.body}".lower()

        best_category = SpamCategory.HAM
        best_matches: list[str] = []

        for concept in SPAM_TAXONOMY:
            hits = [kw for kw in concept.keywords if kw.lower() in text]
            if len(hits) > len(best_matches):
                best_category = concept.category
                best_matches = hits

        is_spam = best_category is not SpamCategory.HAM
        logger.info("[ClassifySpam] category=%s | matches=%s", best_category.value, best_matches)
        return ClassifySpamResponse(
            category=best_category,
            is_spam=is_spam,
            matched_keywords=best_matches,
        )
