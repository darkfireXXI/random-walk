from uuid import uuid4

import pytest
from dao import user_site_relationship as user_site_dao
from db.utils import rw_async_session
from utils.utils import naive_utcnow
from views.relationship import UserSiteRelationshipView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_user_site_relationship():
    user_site_relationship_view = UserSiteRelationshipView(
        uuid=uuid4(),
        from_uuid=uuid4(),
        to_uuid=uuid4(),
        relationship="like",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_category_site = await user_site_dao.insert_user_site_relationship(session, user_site_relationship_view)
        user_site_relationship = await user_site_dao.get_user_site_relationship(
            session,
            inserted_category_site.from_uuid,
            inserted_category_site.to_uuid,
        )

    assert user_site_relationship_view.uuid == user_site_relationship.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_liked_sites(generate_user_site_relationship):
    user_uuid = uuid4()
    user_site_relationship1 = await generate_user_site_relationship(from_uuid=user_uuid, relationship="like")
    await generate_user_site_relationship(from_uuid=user_uuid, relationship="idk_why_im_even_testing_this")
    async with rw_async_session() as session, session.begin():
        user_liked_sites = await user_site_dao.get_user_liked_sites(session, user_uuid)

    assert len(user_liked_sites) == 1
    assert user_liked_sites[0] == user_site_relationship1.to_uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_visited_sites(generate_user_site_relationship):
    user_uuid = uuid4()
    user_site_relationship1 = await generate_user_site_relationship(from_uuid=user_uuid, relationship="visited")
    await generate_user_site_relationship(from_uuid=user_uuid, relationship="like")
    async with rw_async_session() as session, session.begin():
        user_visited_sites = await user_site_dao.get_user_visited_sites(session, user_uuid)

    assert len(user_visited_sites) == 1
    assert user_visited_sites[0] == user_site_relationship1.to_uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user_site_relationship(generate_user_site_relationship):
    user_site_relationship = await generate_user_site_relationship()
    async with rw_async_session() as session, session.begin():
        await user_site_dao.delete_user_site_relationship(session, user_site_relationship.uuid)
        user_site_relationship = await user_site_dao.get_user_site_relationship(
            session,
            user_site_relationship.from_uuid,
            user_site_relationship.to_uuid,
        )

    assert user_site_relationship is None
