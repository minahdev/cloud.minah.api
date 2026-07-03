from __future__ import annotations

import logging

from comm_agent.adapter.inbound.api.schemas.telegram_schema import (
    TelegramIntroduceSchema,
)
from comm_agent.app.dtos.telegram_dto import (
    TelegramResponse,
    TelegramSendCommand,
    TelegramSendQuery,
    TelegramSendResponse,
)
from comm_agent.app.ports.input.telegram_use_case import TelegramUseCase
from comm_agent.app.ports.output.telegram_port import TelegramSenderPort
from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "너는 텔레그램 메시지를 작성하는 비서다. "
    "주어진 주제로 간결하고 친근한 한국어 메시지를 작성해라. "
    "이모지는 최소한으로, 제목이나 머리말 없이 메시지 본문만 출력해라."
)


class TelegramInteractor(TelegramUseCase):
    def __init__(self, telegram_sender: TelegramSenderPort, repository: TelegramSenderPort) -> None:
        self._telegram_sender = telegram_sender
        self._repository = repository

    async def send_message(self, command: TelegramSendCommand) -> TelegramSendResponse:
        orchestrator = FakerOrchestrator(system_prompt=_SYSTEM_PROMPT)
        text = await orchestrator.chat(command.topic)

        await self._telegram_sender.send(chat_id=command.chat_id, text=text)

        logger.info("[Telegram] 발송 완료 | chat_id=%s", command.chat_id)
        return TelegramSendResponse(success=True, chat_id=command.chat_id)

    async def send_report(self, chat_id: str, text: str) -> bool:
        try:
            await self._telegram_sender.send(chat_id=chat_id, text=text)
            logger.info("[Telegram] 업무보고 발송 완료 | chat_id=%s", chat_id)
            return True
        except Exception as e:  # noqa: BLE001 - 보고 실패는 본 작업을 막지 않는다
            logger.warning("[Telegram] 업무보고 실패: %s", e)
            return False

    async def introduce_myself(self, schema: TelegramIntroduceSchema) -> TelegramResponse:

        return await self._repository.introduce_myself(TelegramSendQuery(
            id= schema.id,
            name= schema.name
        ))
