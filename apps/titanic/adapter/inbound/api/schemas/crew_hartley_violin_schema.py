from pydantic import BaseModel, Field

class HartleyViolinSchema(BaseModel):
    
    id: int = Field(0, description="Musician ID")
    name: str = Field("월리스 하틀리", description="Violinist's name")
    # 타이타닉 밴드 마스터 , 배가 가라앉는 순간에도 끝까지 바이올린을 연주함
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Wallace Hartley",
            }
        }
    }