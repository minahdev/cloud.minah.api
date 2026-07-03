"""S3 이미지 저장 어댑터.

- 버킷·리전은 .env 로 설정 (S3_BUCKET, AWS_REGION).
- 자격증명(AWS_ACCESS_KEY_ID/SECRET)은 boto3 기본 체인이 환경변수에서 읽는다.
- boto3(blocking)는 이벤트 루프를 막지 않도록 executor에서 실행한다.
- 클라이언트는 프로세스당 한 번만 생성(lru_cache 싱글톤).
"""

from __future__ import annotations

import asyncio
import logging
import os
import uuid
from functools import lru_cache
from typing import Any

from vision.app.dtos.vision_dto import StoredImage
from vision.app.ports.output.image_storage_port import ImageStoragePort

logger = logging.getLogger(__name__)

_BUCKET = os.getenv("S3_BUCKET", "")
_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
_PREFIX = os.getenv("S3_VISION_PREFIX", "vision").strip("/")
_URL_EXPIRE = int(os.getenv("S3_PRESIGN_EXPIRE", "3600"))  # presigned URL 유효(초)

_EXT_BY_TYPE = {"image/jpeg": ".jpg", "image/png": ".png"}


@lru_cache(maxsize=1)
def _get_client() -> Any:
    import boto3

    logger.info("[S3ImageStorage] 클라이언트 생성 | region=%s bucket=%s", _REGION, _BUCKET)
    return boto3.client("s3", region_name=_REGION)


def _guess_ext(filename: str, content_type: str) -> str:
    name = filename.lower()
    for ext in (".jpg", ".jpeg", ".png"):
        if name.endswith(ext):
            return ext
    return _EXT_BY_TYPE.get(content_type, "")


class S3ImageStorageAdapter(ImageStoragePort):
    async def save(self, *, data: bytes, content_type: str, filename: str) -> StoredImage:
        if not _BUCKET:
            raise RuntimeError("S3_BUCKET 환경변수가 설정되지 않았습니다.")

        key = f"{_PREFIX}/{uuid.uuid4().hex}{_guess_ext(filename, content_type)}"
        client = _get_client()
        loop = asyncio.get_running_loop()

        await loop.run_in_executor(
            None,
            lambda: client.put_object(
                Bucket=_BUCKET,
                Key=key,
                Body=data,
                ContentType=content_type,
            ),
        )
        logger.info("[S3ImageStorage] 저장 완료 | bucket=%s key=%s size=%s", _BUCKET, key, len(data))

        url = ""
        try:
            url = await loop.run_in_executor(
                None,
                lambda: client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": _BUCKET, "Key": key},
                    ExpiresIn=_URL_EXPIRE,
                ),
            )
        except Exception as e:  # noqa: BLE001 - URL 생성 실패는 저장 자체를 막지 않는다
            logger.warning("[S3ImageStorage] presigned URL 생성 실패(무시): %s", e)

        return StoredImage(key=key, url=url)
