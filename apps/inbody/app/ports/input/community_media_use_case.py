from __future__ import annotations

from abc import ABC, abstractmethod

from fastapi import UploadFile

from inbody.app.dtos.community_dto import MediaUploadDto


class CommunityMediaUseCase(ABC):

    @abstractmethod
    async def upload_media(self, user_id: str, file: UploadFile) -> MediaUploadDto:
        pass
