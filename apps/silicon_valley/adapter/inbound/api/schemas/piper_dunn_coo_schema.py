from pydantic import BaseModel, Field

class DunnCooSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("재러드 던", description="Employee's name")
    # Pied Piper COO. 진짜 이름은 Donald Dunn, 리처드에게 헌신적인 운영 책임자

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Jared Dunn",
            }
        }
    }
