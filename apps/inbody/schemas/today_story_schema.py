from pydantic import BaseModel, Field


class TodayStoryPayload(BaseModel):
    userId: str = Field(min_length=1)
    date: str | None = None
    mood: str | None = None
    story: str = ""


class TodayStoryResponse(BaseModel):
    date: str
    mood: str | None = None
    story: str = ""
    updatedAt: str
