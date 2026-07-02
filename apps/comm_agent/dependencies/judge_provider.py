"""심판(Judge) 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(JudgeInteractor)를 직접 알지 못한다.
- 리턴 타입은 포트(JudgeUseCase)로 선언한다.
"""

from comm_agent.app.ports.input.judge_use_case import JudgeUseCase
from comm_agent.app.use_cases.judge_interactor import JudgeInteractor


def get_judge_use_case() -> JudgeUseCase:
    return JudgeInteractor()
