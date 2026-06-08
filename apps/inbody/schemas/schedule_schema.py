from pydantic import BaseModel, Field


class LessonPayload(BaseModel):
    userId: str = Field(min_length=1)
    memberUserId: str | None = None
    id: str = Field(min_length=1)
    date: str
    title: str = ""
    time: str = ""
    scheduleNote: str = ""
    record: dict | None = None
    createdAt: str | None = None


class LessonResponse(BaseModel):
    id: str
    date: str
    title: str
    time: str
    scheduleNote: str
    record: dict | None = None
    createdAt: str
    memberUserId: str
