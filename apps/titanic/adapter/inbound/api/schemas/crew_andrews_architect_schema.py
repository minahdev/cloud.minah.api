from pydantic import BaseModel, Field

class AndrewsArchitectSchema(BaseModel):
    
    id: int = Field(0, description="Architect ID")
    name: str = Field("토마스 앤드류스", description="Architect's name")
    # 타이타닉 설계자 , 배가 침몰할 것을 수학적으로 확신하고 사람들을 도움
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "Thomas Andrews",
            }
        }
    }