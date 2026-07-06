from __future__ import annotations

import asyncio
import logging
import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from vision.adapter.inbound.api.schemas.vision_schema import (
    FaceCandidate,
    FaceRecognizeResponse,
    VisionSchema,
)
from vision.app.dtos.vision_dto import (
    VisionImageCommand,
    VisionIntroduceResponse,
    VisionUploadResponse,
)
from vision.app.dtos.yolo_dto import RecognizeYoloCommand
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.input.yolo_use_case import RecognizeYoloUseCase
from vision.dependencies.vision_provider import get_recognize_use_case, get_vision_use_case

logger = logging.getLogger(__name__)

vision_router = APIRouter(prefix="/vision", tags=["vision"])

# 허용 이미지 타입 (jpg · jpeg · png)
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
_ALLOWED_IMAGE_EXTS = (".jpg", ".jpeg", ".png")

# 얼굴 분류 학습 가중치 (없으면 학습 안내). 필요 시 VISION_FACE_WEIGHTS 로 덮어씀.
_DEFAULT_WEIGHTS = (
    Path(__file__).resolve().parents[4]
    / "resources"
    / "yolo_train"
    / "runs"
    / "yolo11n_face"
    / "weights"
    / "best.pt"
)


def _resolve_weights_path() -> str:
    return os.getenv("VISION_FACE_WEIGHTS", str(_DEFAULT_WEIGHTS))


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


@vision_router.post("/recognize", response_model=FaceRecognizeResponse)
async def recognize_face(
    file: UploadFile = File(...),
    recognizer: RecognizeYoloUseCase = Depends(get_recognize_use_case),
) -> FaceRecognizeResponse:

    filename = file.filename or ""
    content_type = (file.content_type or "").lower()

    is_allowed = content_type in _ALLOWED_IMAGE_TYPES or filename.lower().endswith(_ALLOWED_IMAGE_EXTS)
    if not is_allowed:
        raise HTTPException(status_code=400, detail="jpg, jpeg, png 이미지만 업로드할 수 있습니다.")

    weights_path = _resolve_weights_path()
    if not Path(weights_path).is_file():
        raise HTTPException(
            status_code=503,
            detail="얼굴 인식 모델이 아직 학습되지 않았습니다. yolo_demo.py 로 먼저 학습해 주세요.",
        )

    data = await file.read()

    # 업로드 바이트를 임시 파일로 저장 → YOLO는 경로로 추론한다.
    # ultralytics가 인식하는 확장자로 정규화(.jfif 등은 실제 JPEG → .jpg).
    ext = Path(filename).suffix.lower()
    suffix = ".png" if (ext == ".png" or content_type == "image/png") else ".jpg"
    tmp_path = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        # 모델 로드+추론은 blocking → 이벤트 루프를 막지 않도록 스레드에서 실행
        result = await asyncio.to_thread(
            recognizer.recognize,
            RecognizeYoloCommand(image_path=tmp_path, weights_path=weights_path),
        )
    finally:
        if tmp_path:
            Path(tmp_path).unlink(missing_ok=True)

    return FaceRecognizeResponse(
        name=result.name,
        confidence=result.confidence,
        top5=[FaceCandidate(name=n, prob=p) for n, p in result.top5],
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
