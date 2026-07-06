from __future__ import annotations

from pydantic import BaseModel, Field


class FaceCandidate(BaseModel):
    """얼굴 인식 후보 1건 (인물명 + 확률)."""

    name: str
    prob: float


class FaceRecognizeResponse(BaseModel):
    """얼굴 인식 결과 — 가장 유력한 인물 + 상위 후보."""

    name: str
    confidence: float
    top5: list[FaceCandidate] = Field(default_factory=list)


class VisionSchema(BaseModel):
    id: int = Field(0, description="Vision Agent ID")
    name: str = Field("Vision", description="Vision Agent")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Vision",
            }
        }
    }
