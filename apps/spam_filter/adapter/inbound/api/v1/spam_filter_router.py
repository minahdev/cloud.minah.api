from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from spam_filter.adapter.inbound.api.schemas.classify_spam_schema import ClassifySpamSchema
from spam_filter.app.dtos.classify_spam_dto import ClassifySpamCommand, ClassifySpamResponse
from spam_filter.app.ports.input.classify_spam_use_case import ClassifySpamUseCase
from spam_filter.dependencies.classify_spam_provider import get_classify_spam_use_case

logger = logging.getLogger(__name__)

spam_filter_router = APIRouter(prefix="/spam_filter", tags=["spam_filter"])


@spam_filter_router.post("/classify", response_model=ClassifySpamResponse)
def classify_spam(
    schema: ClassifySpamSchema,
    use_case: ClassifySpamUseCase = Depends(get_classify_spam_use_case),
) -> ClassifySpamResponse:
    """메일 제목·본문을 스팸 온톨로지로 분류한다."""
    return use_case.classify(
        ClassifySpamCommand(subject=schema.subject, body=schema.body)
    )
