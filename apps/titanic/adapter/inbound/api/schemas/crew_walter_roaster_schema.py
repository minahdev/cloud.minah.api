from pydantic import BaseModel, Field

class WalterRoasterSchema(BaseModel):
    
    id: int = Field(0, description="Crew ID")
    name: str = Field("월터 로드 / 화부", description="Crew's name")
    # 타이타닉 기관실 인력. 숨겨진 영웅들인 화부와 불을 끄던 스토커들의 역사적 기록
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": "Walter Lord / Crew",
            }
        }
    }