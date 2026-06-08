from pydantic import BaseModel, Field

class IsidorCoupleSchema(BaseModel):
    
    id: int = Field(0, description="Passenger ID")
    name: str = Field("이시도르 스트라우스", description="Passenger's name")
    # 침대 위의 노부부 남편. 메이시스 백화점 창업자로 아내 이다와 침대에서 함께 마지막을 맞이함
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 8,
                "name": "Isidor Straus",
            }
        }
    }