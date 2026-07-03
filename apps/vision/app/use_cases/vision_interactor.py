from __future__ import annotations

import logging

from vision.adapter.inbound.api.schemas.vision_schema import VisionSchema
from vision.app.dtos.vision_dto import (
    VisionImageCommand,
    VisionIntroduceResponse,
    VisionQuery,
    VisionUploadResponse,
)
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.output.image_storage_port import ImageStoragePort
from vision.app.ports.output.vision_port import VisionPort

logger = logging.getLogger(__name__)


class VisionInteractor(VisionUseCase):
    def __init__(self, repository: VisionPort, storage: ImageStoragePort) -> None:
        self._repository = repository
        self._storage = storage

    async def introduce_myself(self, schema: VisionSchema) -> VisionIntroduceResponse:

        return await self._repository.introduce_myself(VisionQuery(
            id=schema.id,
            name=schema.name,
        ))

    async def upload_image(self, command: VisionImageCommand) -> VisionUploadResponse:
        # 받은 이미지를 스토리지(S3)에 저장하고 참조(key/url)를 돌려준다.
        stored = await self._storage.save(
            data=command.data,
            content_type=command.content_type,
            filename=command.filename,
        )
        logger.info(
            "[Vision] 이미지 저장 | filename=%s type=%s size=%s key=%s",
            command.filename,
            command.content_type,
            command.size,
            stored.key,
        )
        return VisionUploadResponse(
            filename=command.filename,
            content_type=command.content_type,
            size=command.size,
            key=stored.key,
            url=stored.url,
        )
