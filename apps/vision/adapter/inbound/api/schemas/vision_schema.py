from __future__ import annotations

from pydantic import BaseModel, Field


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
