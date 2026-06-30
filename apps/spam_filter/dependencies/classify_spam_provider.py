"""ClassifySpam 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(ClassifySpamInteractor)를 직접 알지 못한다.
- 리턴 타입은 포트(ClassifySpamUseCase)로 선언한다.
"""

from spam_filter.app.ports.input.classify_spam_use_case import ClassifySpamUseCase
from spam_filter.app.use_cases.classify_spam_interactor import ClassifySpamInteractor


def get_classify_spam_use_case() -> ClassifySpamUseCase:
    return ClassifySpamInteractor()
