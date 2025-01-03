from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserView:
    uuid: UUID
    user_name: str
    email: str
    password: str
    photo: str | None
    role: str
    joined_at: datetime
    last_login: datetime


@dataclass
class SiteView:
    uuid: UUID
    url: str
    name: str | None
    status: str | None
    likes: int
    dislikes: int
    collections: int
    score: float
    thumbnail: str | None
    submitted_by: UUID | None
    created_at: datetime
    updated_at: datetime


@dataclass
class CategoryGroupView:
    uuid: UUID
    name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class CategoryView:
    uuid: UUID
    name: str
    parent_uuid: UUID
    parent_name: str
    status: str | None
    created_at: datetime
    updated_at: datetime
