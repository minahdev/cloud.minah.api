from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.vision_dto import StoredImage


class ImageStoragePort(ABC):
    """이미지 저장 게이트웨이 (구현체는 S3 등)."""

    @abstractmethod
    async def save(self, *, data: bytes, content_type: str, filename: str) -> StoredImage:
        pass
