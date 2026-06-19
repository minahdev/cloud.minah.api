from pydantic import BaseModel, Field

class DineshDashSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("디네시 추그타이", description="Employee's name")
    # Pied Piper 백엔드 개발자. 길포일과 끊임없이 경쟁하며 자존심 대결을 벌임

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Dinesh Chugtai",
            }
        }
    }
