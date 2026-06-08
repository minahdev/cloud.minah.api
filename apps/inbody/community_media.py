"""커뮤니티 게시물 사진·동영상 로컬 저장."""

from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

APPS_DIR = Path(__file__).resolve().parents[1]
COMMUNITY_UPLOAD_DIR = APPS_DIR / "uploads" / "community"

IMAGE_TYPES = frozenset({"image/jpeg", "image/png", "image/webp", "image/gif"})
VIDEO_TYPES = frozenset({"video/mp4", "video/webm", "video/quicktime"})
ALLOWED_TYPES = IMAGE_TYPES | VIDEO_TYPES

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_VIDEO_BYTES = 50 * 1024 * 1024
MAX_FILES_PER_POST = 4

EXT_BY_TYPE = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    "video/quicktime": ".mov",
}


def ensure_upload_dir() -> Path:
    COMMUNITY_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return COMMUNITY_UPLOAD_DIR


class CommunityMediaStorage:
    """커뮤니티 첨부 파일 저장 (로컬 디스크). FastAPI DI로 주입."""

    def __init__(self, upload_dir: Path | None = None) -> None:
        self._upload_dir = upload_dir or COMMUNITY_UPLOAD_DIR

    def ensure_dir(self) -> Path:
        self._upload_dir.mkdir(parents=True, exist_ok=True)
        return self._upload_dir

    @staticmethod
    def media_type_for(content_type: str) -> str:
        if content_type in IMAGE_TYPES:
            return "image"
        if content_type in VIDEO_TYPES:
            return "video"
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    async def save(self, file: UploadFile) -> dict[str, str]:
        content_type = (file.content_type or "").split(";")[0].strip().lower()
        if content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

        data = await file.read()
        max_bytes = MAX_VIDEO_BYTES if content_type in VIDEO_TYPES else MAX_IMAGE_BYTES
        if len(data) > max_bytes:
            raise HTTPException(
                status_code=400,
                detail="파일 크기가 너무 큽니다. (사진 10MB, 동영상 50MB 이하)",
            )
        if not data:
            raise HTTPException(status_code=400, detail="빈 파일입니다.")

        ext = EXT_BY_TYPE.get(content_type, ".bin")
        name = f"{uuid.uuid4().hex}{ext}"
        dest = self.ensure_dir() / name
        dest.write_bytes(data)

        return {
            "url": f"/uploads/community/{name}",
            "type": self.media_type_for(content_type),
        }


_default_storage = CommunityMediaStorage()


def get_community_media_storage() -> CommunityMediaStorage:
    """앱 전역 싱글톤 (Keymaker 패턴과 동일)."""
    return _default_storage
