from pydantic import BaseModel, Field

class CalTesterSchema(BaseModel):
    
    id: int = Field(0, description="Passenger ID")
    name: str = Field("칼 헉클리", description="Passenger's name")
    # 로즈의 오만한 약혼자. 1등석 승객이자 재력가로 잭과 대립하며 테스트 성격의 악역을 맡음
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 7,
                "name": "Caledon Hockley",
            }
        }
    }