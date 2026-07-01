"""ComposeEmail 오케스트레이터 의존성 조립소 (Hub).

- Hub는 comm_agent의 '포트'(ComposeAndSendEmailUseCase)만 타입으로 의존한다.
- 구현체 조립은 comm_agent의 프로바이더를 재사용한다 (Hub→Spoke port only).
"""

from fastapi import Depends

from comm_agent.app.ports.input.email_send_use_case import ComposeAndSendEmailUseCase
from comm_agent.dependencies.email_send_provider import get_compose_and_send_email_use_case

from star_craft.app.use_cases.compose_email_orchestrator import ComposeEmailOrchestrator


def get_compose_email_orchestrator(
    email_use_case: ComposeAndSendEmailUseCase = Depends(get_compose_and_send_email_use_case),
) -> ComposeEmailOrchestrator:
    return ComposeEmailOrchestrator(email_use_case=email_use_case)
