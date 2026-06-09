from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from inbody.community_media import CommunityMediaStorage, get_community_media_storage
from inbody.controllers.community_controller import CommunityController


def inject_community_media_storage() -> CommunityMediaStorage:
    """FastAPI DI: 커뮤니티 미디어 저장소."""
    return get_community_media_storage()


async def get_community_controller(
    db: AsyncSession = Depends(get_db),
    media_storage: CommunityMediaStorage = Depends(inject_community_media_storage),
) -> CommunityController:
    return CommunityController(db, media_storage)
