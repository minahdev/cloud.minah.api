from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from vision.adapter.inbound.api.schemas.vision_schema import VisionSchema
from vision.app.dtos.vision_dto import (
    VisionImageCommand,
    VisionIntroduceResponse,
    VisionUploadResponse,
)
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.dependencies.vision_provider import get_vision_use_case

logger = logging.getLogger(__name__)

vision_router = APIRouter(prefix="/vision", tags=["vision"])

# 허용 이미지 타입 (jpg · jpeg · png)
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
_ALLOWED_IMAGE_EXTS = (".jpg", ".jpeg", ".png")


@vision_router.post("/upload", response_model=VisionUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    vision: VisionUseCase = Depends(get_vision_use_case)) -> VisionUploadResponse:

    filename = file.filename or ""
    content_type = (file.content_type or "").lower()

    is_allowed = content_type in _ALLOWED_IMAGE_TYPES or filename.lower().endswith(_ALLOWED_IMAGE_EXTS)
    if not is_allowed:
        raise HTTPException(status_code=400, detail="jpg, jpeg, png 이미지만 업로드할 수 있습니다.")

    data = await file.read()

    return await vision.upload_image(
        VisionImageCommand(
            filename=filename,
            content_type=content_type,
            size=len(data),
            data=data,
        )
    )


@vision_router.get("/myself", response_model=VisionIntroduceResponse)
async def introduce_myself(
    vision: VisionUseCase = Depends(get_vision_use_case)) -> VisionIntroduceResponse:

    return await vision.introduce_myself(
        VisionSchema(
            id=1,
            name="Vision",
        )
    )
