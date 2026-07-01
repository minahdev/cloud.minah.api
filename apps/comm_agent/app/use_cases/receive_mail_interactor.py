from __future__ import annotations

import logging

from comm_agent.app.dtos.received_mail_dto import ReceivedMailCommand, ReceivedMailView
from comm_agent.app.ports.input.receive_mail_use_case import ReceiveMailUseCase
from comm_agent.app.ports.output.received_mail_port import ReceivedMailRepositoryPort

logger = logging.getLogger(__name__)


class ReceiveMailInteractor(ReceiveMailUseCase):
    def __init__(self, repository: ReceivedMailRepositoryPort) -> None:
        self._repository = repository

    async def save_incoming(self, command: ReceivedMailCommand) -> int:
        mail_id = await self._repository.save_mail(command)
        logger.info("[ReceiveMail] 메일 저장 | id=%s from=%s", mail_id, command.sender)
        return mail_id

    async def list_received(self) -> list[ReceivedMailView]:
        return await self._repository.list_mails()
