from __future__ import annotations

from fastapi import UploadFile

from inbody.app.dtos.community_dto import MediaUploadDto
from inbody.app.ports.output.community_media_port import CommunityMediaPort
from inbody.community_media import CommunityMediaStorage


class CommunityMediaLocalAdapter(CommunityMediaPort):

    def __init__(self, storage: CommunityMediaStorage) -> None:
        self._storage = storage

    async def save(self, file: UploadFile) -> MediaUploadDto:
        result = await self._storage.save(file)
        return MediaUploadDto(url=result["url"], type=result["type"])
