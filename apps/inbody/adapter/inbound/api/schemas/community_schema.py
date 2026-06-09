from typing import Literal

from pydantic import BaseModel, Field


class CommunityMediaItem(BaseModel):
    url: str = Field(min_length=1)
    type: Literal["image", "video"]


class CommunityPostCreate(BaseModel):
    userId: str = Field(min_length=1)
    workoutType: str = "기타"
    content: str = ""
    distanceKm: float | None = None
    durationMin: int | None = None
    calories: int | None = None
    media: list[CommunityMediaItem] = Field(default_factory=list)


class CommunityPostResponse(BaseModel):
    id: str
    authorId: str
    workoutType: str
    content: str
    createdAt: str
    distanceKm: float | None = None
    durationMin: int | None = None
    calories: int | None = None
    media: list[CommunityMediaItem] = Field(default_factory=list)
    cheerCount: int = 0
    commentCount: int = 0
    cheeredByMe: bool = False


class CommunityMediaUploadResponse(BaseModel):
    url: str
    type: Literal["image", "video"]


class CommunityCheerRequest(BaseModel):
    userId: str = Field(min_length=1)


class CommunityCheerResponse(BaseModel):
    cheerCount: int
    cheeredByMe: bool


class CommunityCommentCreate(BaseModel):
    userId: str = Field(min_length=1)
    content: str = Field(min_length=1, max_length=1000)


class CommunityCommentResponse(BaseModel):
    id: str
    authorId: str
    content: str
    createdAt: str
