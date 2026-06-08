from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class TitanicRecordSchema(BaseModel):
    """Titanic CSV 1행 — Sex 컬럼은 API 필드 `gender`로 매핑."""

    model_config = ConfigDict(populate_by_name=True)

    passenger_id: str = Field(validation_alias=AliasChoices("PassengerId", "passengerId"))
    survived: str = Field(
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
    cabin: str = Field(default="", validation_alias=AliasChoices("Cabin", "cabin"))
    embarked: str = Field(
        default="",
        validation_alias=AliasChoices("Embarked", "embarked"),
    )


class JamesUploadResponse(BaseModel):
    """POST /titanic/james/upload 응답."""

    saved: int
    received: int
    message: str = "업로드가 완료되었습니다."
