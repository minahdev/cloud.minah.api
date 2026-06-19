from pydantic import BaseModel, Field

class BighettiHrSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("넬슨 비게티", description="Employee's name")
    # Big Head. Hooli 공동창업자 명예직, 리처드의 절친이자 우연히 성공한 인물

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "Nelson Bighetti",
            }
        }
    }
