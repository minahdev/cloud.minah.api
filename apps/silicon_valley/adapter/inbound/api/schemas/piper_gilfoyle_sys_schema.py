from pydantic import BaseModel, Field

class GilfoyleSysSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("버트람 길포일", description="Employee's name")
    # Pied Piper 시스템 아키텍트. 사탄 숭배자이며 보안과 인프라의 달인

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Bertram Gilfoyle",
            }
        }
    }
