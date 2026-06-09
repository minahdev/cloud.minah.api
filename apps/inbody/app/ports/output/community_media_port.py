from __future__ import annotations

from abc import ABC, abstractmethod

from fastapi import UploadFile

from inbody.app.dtos.community_dto import MediaUploadDto


class CommunityMediaPort(ABC):

    @abstractmethod
    async def save(self, file: UploadFile) -> MediaUploadDto:
        pass
