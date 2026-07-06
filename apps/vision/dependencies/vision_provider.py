"""
Vision 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(VisionRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(VisionUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from vision.adapter.outbound.repositories.vision_repository import VisionRepository
from vision.adapter.outbound.storage.s3_image_storage_adapter import S3ImageStorageAdapter
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.input.yolo_use_case import RecognizeYoloUseCase
from vision.app.ports.output.image_storage_port import ImageStoragePort
from vision.app.ports.output.vision_port import VisionPort
from vision.app.use_cases.vision_interactor import VisionInteractor
from vision.app.use_cases.yolo_interactor import RecognizeYoloInteractor


def get_vision_repository(
    db: AsyncSession = Depends(get_db),
) -> VisionPort:
    return VisionRepository(session=db)


def get_image_storage() -> ImageStoragePort:
    return S3ImageStorageAdapter()


def get_vision_use_case(
    repository: VisionPort = Depends(get_vision_repository),
    storage: ImageStoragePort = Depends(get_image_storage),
) -> VisionUseCase:
    return VisionInteractor(repository=repository, storage=storage)


def get_recognize_use_case() -> RecognizeYoloUseCase:
    return RecognizeYoloInteractor()
