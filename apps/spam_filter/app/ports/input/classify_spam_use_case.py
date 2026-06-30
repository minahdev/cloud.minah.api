from __future__ import annotations

from abc import ABC, abstractmethod

from spam_filter.app.dtos.classify_spam_dto import ClassifySpamCommand, ClassifySpamResponse


class ClassifySpamUseCase(ABC):
    """메일을 스팸 온톨로지에 따라 분류한다."""

    @abstractmethod
    def classify(self, command: ClassifySpamCommand) -> ClassifySpamResponse:
        pass
