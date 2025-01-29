import sqlalchemy
from db.models.base import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column
from views.main import CategoryGroupView, CategoryView, SiteView, UserView


class User(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("user_name", name="user_name_key"),)

    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    user_name = mapped_column(sqlalchemy.Text(), nullable=False, index=True)
    email = mapped_column(sqlalchemy.Text(), nullable=False)
    password = mapped_column(sqlalchemy.Text(), nullable=False)
    # "" != None in postgres/sqlalchemy
    photo = mapped_column(sqlalchemy.Text(), nullable=True)
    role = mapped_column(sqlalchemy.Text(), nullable=False)
    joined_at = mapped_column(TIMESTAMP, nullable=False)
    last_login = mapped_column(TIMESTAMP, nullable=False)

    def to_view(self):
        return UserView(
            uuid=self.uuid,
            user_name=self.user_name,
            email=self.email,
            password=self.password,
            photo=self.photo,
            role=self.role,
            joined_at=self.joined_at,
            last_login=self.last_login,
        )


class Site(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("url", name="url_key"),)
    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    url = mapped_column(sqlalchemy.Text(), nullable=False)
    name = mapped_column(sqlalchemy.Text(), nullable=True)
    status = mapped_column(sqlalchemy.Text(), nullable=True)
    likes = mapped_column(sqlalchemy.Integer(), nullable=False)
    dislikes = mapped_column(sqlalchemy.Integer(), nullable=False)
    collections = mapped_column(sqlalchemy.Integer(), nullable=False)
    score = mapped_column(sqlalchemy.Float(), nullable=False)
    thumbnail = mapped_column(sqlalchemy.Text(), nullable=True)
    submitted_by = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=True)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)

    def to_view(self):
        return SiteView(
            uuid=self.uuid,
            url=self.url,
            name=self.name,
            status=self.status,
            likes=self.likes,
            dislikes=self.dislikes,
            collections=self.collections,
            score=self.score,
            thumbnail=self.thumbnail,
            submitted_by=self.submitted_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class CategoryGroup(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("name", name="category_group_name_key"),)
    # https://zipso.net/big-list-of-all-stumbleupon-categories-2014/
    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    name = mapped_column(sqlalchemy.Text(), nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)

    def to_view(self):
        return CategoryGroupView(
            uuid=self.uuid,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class Category(Base):
    __table_args__ = (sqlalchemy.UniqueConstraint("name", name="category_name_key"),)

    uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False, primary_key=True)
    name = mapped_column(sqlalchemy.Text(), nullable=False, index=True)
    parent_uuid = mapped_column(sqlalchemy.UUID(as_uuid=True), nullable=False)
    parent_name = mapped_column(sqlalchemy.Text(), nullable=False)
    status = mapped_column(sqlalchemy.Text(), nullable=True)
    created_at = mapped_column(TIMESTAMP, nullable=False)
    updated_at = mapped_column(TIMESTAMP, nullable=False)

    def to_view(self):
        return CategoryView(
            uuid=self.uuid,
            name=self.name,
            parent_uuid=self.parent_uuid,
            parent_name=self.parent_name,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
