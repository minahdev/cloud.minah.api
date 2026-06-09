from __future__ import annotations

import logging

from fastapi import UploadFile

from inbody.app.dtos.community_dto import MediaUploadDto
from inbody.app.ports.input.community_media_use_case import CommunityMediaUseCase
from inbody.app.ports.output.community_media_port import CommunityMediaPort
from inbody.app.ports.output.user_lookup_port import UserLookupPort

logger = logging.getLogger(__name__)


class CommunityMediaInteractor(CommunityMediaUseCase):

    def __init__(
        self,
        media_port: CommunityMediaPort,
        user_lookup: UserLookupPort,
    ) -> None:
        self._media = media_port
        self._users = user_lookup

    async def upload_media(self, user_id: str, file: UploadFile) -> MediaUploadDto:
        await self._users.require_by_login_id(user_id)
        return await self._media.save(file)
