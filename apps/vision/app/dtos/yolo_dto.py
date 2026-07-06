"""YOLO 얼굴 분류 학습·추론용 DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TrainYoloCommand:
    """파인튜닝 하이퍼파라미터."""

    epochs: int = 10
    batch: int = 16
    imgsz: int = 224              # 분류 모델 기본 입력 크기
    device: str = "cpu"          # GPU면 "0", 맥북이면 "mps"
    project: str = ""            # 결과 저장 위치(비면 ultralytics 기본값)
    name: str = "yolo11n_face"   # 실행 이름(runs/<name>)


@dataclass
class TrainYoloResult:
    """학습 결과 — 저장된 가중치 경로와 클래스 목록."""

    weights_path: str
    save_dir: str
    classes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RecognizeYoloCommand:
    """추론 요청 — 이미지 1장 + 사용할 가중치."""

    image_path: str
    weights_path: str


@dataclass
class RecognizeYoloResult:
    """추론 결과 — 가장 유력한 인물 + 상위 후보."""

    name: str
    confidence: float
    top5: list[tuple[str, float]] = field(default_factory=list)
