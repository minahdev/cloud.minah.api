from pydantic import BaseModel, Field

class MollyScalerSchema(BaseModel):
    
    id: int = Field(0, description="Passenger ID")
    name: str = Field("몰리 브라운", description="Passenger's name")
    # 침몰하지 않는 몰리 브라운. 신흥 귀족 출신으로 6호 구명보트를 직접 지휘하며 승객들을 격려함
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 10,
                "name": "Margaret 'Molly' Brown",
            }
        }
    }