from __future__ import annotations

from typing import Optional
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

class JamesDirectorSchema(BaseModel):
    id: int = Field(0, description="Musician ID")
    name: str = Field("제임스 카메론", description="Titanic Director")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "James Carmeron",
            }
        }
    }




class TitanicRecordSchema(BaseModel):
    """Titanic CSV 1행 — Sex 컬럼은 API 필드 `gender`로 매핑."""

    model_config = ConfigDict(populate_by_name=True)

    passenger_id: str = Field(validation_alias=AliasChoices("PassengerId", "passengerId"))
    survived: Optional[str] = Field(
        default="",
        validation_alias=AliasChoices("Survived", "survived"),
    )
    pclass: str = Field(default="", validation_alias=AliasChoices("Pclass", "pclass"))
    name: str = Field(default="", validation_alias=AliasChoices("Name", "name"))
    gender: str = Field(
        default="",
        validation_alias=AliasChoices("gender", "Gender", "Sex", "sex"),
    )
    age: str = Field(default="", validation_alias=AliasChoices("Age", "age"))
    sib_sp: str = Field(default="", validation_alias=AliasChoices("SibSp", "sibSp"))
    parch: str = Field(default="", validation_alias=AliasChoices("Parch", "parch"))
    ticket: str = Field(default="", validation_alias=AliasChoices("Ticket", "ticket"))
    fare: str = Field(default="", validation_alias=AliasChoices("Fare", "fare"))
    cabin: Optional[str] = Field(default="", validation_alias=AliasChoices("Cabin", "cabin"))
    embarked: str = Field(
        default="",
        validation_alias=AliasChoices("Embarked", "embarked"),
    )


class JamesUploadResponse(BaseModel):
    """POST /titanic/james/upload 응답."""

    saved: int
    received: int
    message: str = "업로드가 완료되었습니다."


FileUploadSchema = TitanicRecordSchema
