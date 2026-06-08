from pydantic import BaseModel, Field

class SmithCaptainSchema(BaseModel):
    
    id: int = Field(0, description="Captain ID")
    name: str = Field("에드워드 스미스", description="Captain's name")
    # 타이타닉 선장. 백만장자들의 선장이라 불렸으며 고조되는 위기 속에 배와 운명을 함께함
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Edward Smith",
            }
        }
    }