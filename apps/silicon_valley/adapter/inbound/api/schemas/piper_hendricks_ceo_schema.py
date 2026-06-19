from pydantic import BaseModel, Field

class HendricksCeoSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("리처드 헨드릭스", description="Employee's name")
    # Pied Piper CEO. 중간값 압축 알고리즘 발명자, 천재 개발자이자 스타트업 대표

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Richard Hendricks",
            }
        }
    }
