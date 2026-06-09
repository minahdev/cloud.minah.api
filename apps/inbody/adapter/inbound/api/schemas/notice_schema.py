from pydantic import BaseModel, Field


class NoticeCreate(BaseModel):
    userId: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class NoticeResponse(BaseModel):
    id: str
    title: str
    body: str
    authorId: str
    createdAt: str
