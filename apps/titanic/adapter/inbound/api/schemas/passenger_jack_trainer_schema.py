from typing import Any, Optional

from pydantic import BaseModel, Field

class JackTrainerSchema(BaseModel):
    
    id: int = Field(0, description="Passenger ID")
    name: str = Field("잭 도슨", description="Passenger's name")
    # 자유로운 영혼의 3등석 화가. 로즈에게 진정한 삶을 가르쳐준 인물이자 타이타닉 생존 스토리의 주역
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 9,
                "name": "Jack Dawson",
            }
        }
    }
