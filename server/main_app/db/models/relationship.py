import sqlalchemy
from db.models.base import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column
from views.relationship import CategorySiteRelationshipView, UserCategoryRelationshipView, UserSiteRelationshipView


class CategorySiteRelationship(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("from_uuid", "to_uuid", "relationship", name="category_site_id_key"),)

    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    from_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, index=True)
    to_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, index=True)
    relationship = mapped_column(sqlalchemy.Text(), nullable=False)
    status = mapped_column(sqlalchemy.Text(), nullable=True)
    submitted_by = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=True)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)

    def to_view(self):
        return CategorySiteRelationshipView(
            uuid=self.uuid,
            from_uuid=self.from_uuid,
            to_uuid=self.to_uuid,
            relationship=self.relationship,
            status=self.status,
            submitted_by=self.submitted_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class UserCategoryRelationship(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("from_uuid", "to_uuid", "relationship", name="user_category_id_key"),)

    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    from_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, index=True)
    to_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, index=True)
    relationship = mapped_column(sqlalchemy.Text(), nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)

    def to_view(self):
        return UserCategoryRelationshipView(
            uuid=self.uuid,
            from_uuid=self.from_uuid,
            to_uuid=self.to_uuid,
            relationship=self.relationship,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class UserSiteRelationship(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("from_uuid", "to_uuid", "relationship", name="user_site_id_key"),)

    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    from_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, index=True)
    to_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, index=True)
    relationship = mapped_column(sqlalchemy.Text(), nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)

    def to_view(self):
        return UserSiteRelationshipView(
            uuid=self.uuid,
            from_uuid=self.from_uuid,
            to_uuid=self.to_uuid,
            relationship=self.relationship,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
