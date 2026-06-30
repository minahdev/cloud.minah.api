"""Telegram 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(TelegramApiAdapter)를 직접 알지 못한다.
- 리턴 타입은 포트(TelegramUseCase)로 선언한다.
"""

from fastapi import Depends

from comm_agent.adapter.outbound.n8n.n8n_telegram_adapter import N8nTelegramAdapter
from comm_agent.app.ports.input.telegram_use_case import TelegramUseCase
from comm_agent.app.ports.output.telegram_port import TelegramSenderPort
from comm_agent.app.use_cases.telegram_interactor import TelegramInteractor


def get_telegram_sender() -> TelegramSenderPort:
    return N8nTelegramAdapter()


def get_telegram_use_case(
    telegram_sender: TelegramSenderPort = Depends(get_telegram_sender),
) -> TelegramUseCase:
    return TelegramInteractor(telegram_sender=telegram_sender)
