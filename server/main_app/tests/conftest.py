from uuid import uuid4

import pytest
import pytest_asyncio
from dao import category as category_dao
from dao import category_group as category_group_dao
from dao import category_site_relationship as category_site_dao
from dao import site as site_dao
from dao import user as user_dao
from dao import user_category_relationship as user_category_dao
from dao import user_site_relationship as user_site_dao
from db.clear_db import clear_db
from db.utils import rw_async_session
from utils.utils import naive_utcnow
from views.main import CategoryGroupView, CategoryView, SiteView, UserView
from views.relationship import CategorySiteRelationshipView, UserCategoryRelationshipView, UserSiteRelationshipView


@pytest.fixture(scope="function")
def clean_db():
    clear_db()


@pytest_asyncio.fixture(scope="session")
async def generate_user():
    return _generate_user


async def _generate_user(
    uuid=None,
    user_name="drip___drop",
    email="nah@hellyeah.com",
    password="passw0rd",
    photo=None,
    role="default",
    joined_at=None,
    last_login=None,
):
    user_view = UserView(
        uuid=uuid if uuid else uuid4(),
        user_name="drip___drop",
        email="nah@hellyeah.com",
        password="passw0rd",
        photo=None,
        role="default",
        joined_at=joined_at if joined_at else naive_utcnow(),
        last_login=last_login if last_login else naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        user = await user_dao.insert_user(session, user_view)

    return user


@pytest_asyncio.fixture(scope="session")
async def generate_site():
    return _generate_site


async def _generate_site(
    uuid=None,
    url="www.coolest-site-ever.com",
    name=None,
    status=None,
    likes=0,
    dislikes=0,
    collections=0,
    score=0,
    thumbnail=None,
    submitted_by=None,
    created_at=None,
    updated_at=None,
):
    site_view = SiteView(
        uuid=uuid if uuid else uuid4(),
        url=url,
        name=name,
        status=status,
        likes=likes,
        dislikes=dislikes,
        collections=collections,
        score=score,
        thumbnail=thumbnail,
        submitted_by=submitted_by,
        created_at=created_at if created_at else naive_utcnow(),
        updated_at=updated_at if updated_at else naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        site = await site_dao.insert_site(session, site_view)

    return site


@pytest_asyncio.fixture(scope="session")
async def generate_category_group():
    return _generate_category_group


async def _generate_category_group(
    uuid=None,
    name="cool",
    created_at=None,
    updated_at=None,
):
    category_group_view = CategoryGroupView(
        uuid=uuid if uuid else uuid4(),
        name=name,
        created_at=created_at if created_at else naive_utcnow(),
        updated_at=updated_at if updated_at else naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        category_group = await category_group_dao.insert_category_group(session, category_group_view)

    return category_group


@pytest_asyncio.fixture(scope="session")
async def generate_category():
    return _generate_category


async def _generate_category(
    uuid=None,
    name="cool stuff",
    parent_uuid=None,
    parent_name="cool",
    status=None,
    created_at=None,
    updated_at=None,
):
    category_view = CategoryView(
        uuid=uuid if uuid else uuid4(),
        name=name,
        parent_uuid=parent_uuid if parent_uuid else uuid4(),
        parent_name=parent_name,
        status=status,
        created_at=created_at if created_at else naive_utcnow(),
        updated_at=updated_at if updated_at else naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        category = await category_dao.insert_category(session, category_view)

    return category


@pytest_asyncio.fixture(scope="session")
async def generate_category_site_relationship():
    return _generate_category_site_relationship


async def _generate_category_site_relationship(
    uuid=None,
    from_uuid=None,
    to_uuid=None,
    relationship="tag",
    status=None,
    created_at=None,
    updated_at=None,
):
    category_site_view = CategorySiteRelationshipView(
        uuid=uuid if uuid else uuid4(),
        from_uuid=from_uuid if from_uuid else uuid4(),
        to_uuid=to_uuid if to_uuid else uuid4(),
        relationship=relationship,
        status=status,
        created_at=created_at if created_at else naive_utcnow(),
        updated_at=updated_at if updated_at else naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        category_site_relationship = await category_site_dao.insert_category_site_relationship(
            session, category_site_view
        )

    return category_site_relationship


@pytest_asyncio.fixture(scope="session")
async def generate_user_category_relationship():
    return _generate_user_category_relationship


async def _generate_user_category_relationship(
    uuid=None,
    from_uuid=None,
    to_uuid=None,
    relationship="like",
    created_at=None,
    updated_at=None,
):
    user_category_view = UserCategoryRelationshipView(
        uuid=uuid if uuid else uuid4(),
        from_uuid=from_uuid if from_uuid else uuid4(),
        to_uuid=to_uuid if to_uuid else uuid4(),
        relationship=relationship,
        created_at=created_at if created_at else naive_utcnow(),
        updated_at=updated_at if updated_at else naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        user_category_relationship = await user_category_dao.insert_user_category_relationship(
            session, user_category_view
        )

    return user_category_relationship


@pytest_asyncio.fixture(scope="session")
async def generate_user_site_relationship():
    return _generate_user_site_relationship


async def _generate_user_site_relationship(
    uuid=None,
    from_uuid=None,
    to_uuid=None,
    relationship="like",
    created_at=None,
    updated_at=None,
):
    user_site_view = UserSiteRelationshipView(
        uuid=uuid if uuid else uuid4(),
        from_uuid=from_uuid if from_uuid else uuid4(),
        to_uuid=to_uuid if to_uuid else uuid4(),
        relationship=relationship,
        created_at=created_at if created_at else naive_utcnow(),
        updated_at=updated_at if updated_at else naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        user_site_relationship = await user_site_dao.insert_user_site_relationship(session, user_site_view)

    return user_site_relationship
