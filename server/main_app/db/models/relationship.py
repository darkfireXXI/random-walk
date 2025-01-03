import sqlalchemy
from db.models.base import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column


class CategorySiteRelationship(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("from_uuid", "to_uuid", "relationship", name="category_site_id_key"),)

    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    from_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False)
    to_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False)
    relationship = mapped_column(sqlalchemy.Text(), nullable=False)
    status = mapped_column(sqlalchemy.Text(), nullable=True)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)


class UserCategoryRelationship(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("from_uuid", "to_uuid", "relationship", name="user_category_id_key"),)

    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    from_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False)
    to_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False)
    relationship = mapped_column(sqlalchemy.Text(), nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)


class UserSiteRelationship(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("from_uuid", "to_uuid", "relationship", name="user_site_id_key"),)

    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    from_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False)
    to_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False)
    relationship = mapped_column(sqlalchemy.Text(), nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)
