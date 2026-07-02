from __future__ import annotations

import logging

from comm_agent.adapter.inbound.api.schemas.receive_mail_schema import (
    ReceivedMailIntroduceSchema,
)
from comm_agent.app.dtos.received_mail_dto import (
    ReceivedMailCommand,
    ReceivedMailResponse,
    ReceivedMailView,
)
from comm_agent.app.ports.input.received_mail_use_case import ReceiveMailUseCase
from comm_agent.app.ports.output.embedding_port import EmbeddingPort
from comm_agent.app.ports.output.received_mail_port import ReceivedMailRepositoryPort

logger = logging.getLogger(__name__)


class ReceiveMailInteractor(ReceiveMailUseCase):
    def __init__(
        self,
        repository: ReceivedMailRepositoryPort,
        embedding_port: EmbeddingPort,
    ) -> None:
        self._repository = repository
        self._embedding_port = embedding_port

    async def save_incoming(self, command: ReceivedMailCommand) -> int:
        # 메일 내용(제목+본문)을 임베딩 벡터로 변환한 뒤 pgvector에 저장한다.
        content = f"{command.subject}\n\n{command.body}".strip()
        embedding = await self._embedding_port.embed(content)
        mail_id = await self._repository.save_mail(command, embedding)
        logger.info("[ReceiveMail] 메일 저장 | id=%s from=%s", mail_id, command.sender)
        return mail_id

    async def list_received(self) -> list[ReceivedMailView]:
        return await self._repository.list_mails()

    async def introduce_myself(self, schema: ReceivedMailIntroduceSchema) -> ReceivedMailResponse:
        logger.info("[ReceiveMail] introduce_myself | id=%s name=%s", schema.id, schema.name)
        return ReceivedMailResponse(
            id=schema.id,
            name=schema.name,
            answer=(
                f"안녕하세요, 저는 '{schema.name}'입니다. "
                "n8n이 감지한 수신 메일을 저장하고 임베딩(pgvector)으로 보관합니다."
            ),
        )
