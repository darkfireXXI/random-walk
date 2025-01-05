from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CategorySiteRelationshipView:
    uuid: UUID
    from_uuid: UUID
    to_uuid: UUID
    relationship: str
    status: str | None
    submitted_by: UUID | None
    created_at: datetime
    updated_at: datetime


@dataclass
class UserCategoryRelationshipView:
    uuid: UUID
    from_uuid: UUID
    to_uuid: UUID
    relationship: str
    created_at: datetime
    updated_at: datetime


@dataclass
class UserSiteRelationshipView:
    uuid: UUID
    from_uuid: UUID
    to_uuid: UUID
    relationship: str
    created_at: datetime
    updated_at: datetime
