"""ComposeAndSendEmail 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(N8nEmailAdapter)를 직접 알지 못한다.
- 리턴 타입은 포트(ComposeAndSendEmailUseCase)로 선언한다.
"""

from fastapi import Depends

from comm_agent.adapter.outbound.n8n.n8n_email_adapter import N8nEmailAdapter
from comm_agent.app.ports.input.email_send_use_case import ComposeAndSendEmailUseCase
from comm_agent.app.ports.output.email_send_port import EmailSenderPort
from comm_agent.app.use_cases.email_send_interactor import ComposeAndSendEmailInteractor


def get_email_sender() -> EmailSenderPort:
    return N8nEmailAdapter()


def get_compose_and_send_email_use_case(
    email_sender: EmailSenderPort = Depends(get_email_sender),
) -> ComposeAndSendEmailUseCase:
    return ComposeAndSendEmailInteractor(email_sender=email_sender)
