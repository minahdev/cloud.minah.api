from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MediaItemDto:
    url: str
    type: str  # "image" | "video"


@dataclass
class PostCreateCommand:
    user_id: str
    workout_type: str
    content: str
    media: list[MediaItemDto] = field(default_factory=list)
    distance_km: float | None = None
    duration_min: int | None = None
    calories: int | None = None


@dataclass
class PostDto:
    id: str
    author_id: str
    workout_type: str
    content: str
    created_at: str
    cheer_count: int = 0
    comment_count: int = 0
    cheered_by_me: bool = False
    media: list[MediaItemDto] = field(default_factory=list)
    distance_km: float | None = None
    duration_min: int | None = None
    calories: int | None = None


@dataclass
class CheerCommand:
    post_id: int
    user_id: str


@dataclass
class CheerDto:
    cheer_count: int
    cheered_by_me: bool


@dataclass
class CommentCreateCommand:
    post_id: int
    user_id: str
    content: str


@dataclass
class CommentDto:
    id: str
    author_id: str
    content: str
    created_at: str


@dataclass
class MediaUploadCommand:
    user_id: str


@dataclass
class MediaUploadDto:
    url: str
    type: str
