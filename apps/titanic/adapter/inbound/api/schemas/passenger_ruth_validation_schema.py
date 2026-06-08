from pydantic import BaseModel, Field

class RuthValidationSchema(BaseModel):
    
    id: int = Field(0, description="Passenger ID")
    name: str = Field("루쓰 드윗 부카터", description="Passenger's name")
    # 로즈의 어머니. 류사회의 격식과 가문의 재정적 생존(밸리데이션)을 강요했던 엄격한 인물
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 12,
                "name": "Ruth DeWitt Bukater",
            }
        }
    }