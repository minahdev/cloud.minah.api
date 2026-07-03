from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)  # 생성 후 수정 불가하도록 설정
class VisionQuery:
    id: int
    name: str


@dataclass
class VisionIntroduceResponse:
    """비전 자기소개 응답 (JamesIntroduceResponse 대응)."""

    id: int
    name: str
    answer: str = ""


@dataclass
class VisionImageCommand:
    """업로드된 이미지 1건 (원본 바이트 포함)."""

    filename: str
    content_type: str
    size: int
    data: bytes


@dataclass
class StoredImage:
    """스토리지에 저장된 이미지 참조."""

    key: str
    url: str = ""  # 조회용 presigned URL (버킷 private — 한시적)


@dataclass
class VisionUploadResponse:
    """이미지 저장 결과."""

    filename: str
    content_type: str
    size: int
    key: str = ""
    url: str = ""
    message: str = "이미지를 저장했습니다."
