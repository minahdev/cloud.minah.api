from pydantic import BaseModel, Field

class RoseModelSchema(BaseModel):
    
    id: int = Field(0, description="Passenger ID")
    name: str = Field("로즈 드윗 부카터", description="Passenger's name")
    # 타이타닉의 실질적 모델이자 주인공. 104세의 생존자로 비아트리스 우드를 모티브 삼아 자유를 갈망한 인물
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "name": "Rose DeWitt Bukater",
            }
        }
    }