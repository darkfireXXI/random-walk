from uuid import uuid4

import pytest
from api import user_site_relationship as user_site_api
from db.utils import ro_async_session, rw_async_session
from utils.utils import naive_utcnow
from views.relationship import UserSiteRelationshipView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_liked_sites(generate_user_site_relationship):
    user_uuid = uuid4()
    user_site_relationship1 = await generate_user_site_relationship(from_uuid=user_uuid)
    user_site_relationship2 = await generate_user_site_relationship(from_uuid=user_uuid)
    async with ro_async_session() as session:
        user_liked_sites = await user_site_api.get_user_liked_sites(session, user_uuid)

    assert len(user_liked_sites) == 2
    assert user_liked_sites[0] == user_site_relationship2.to_uuid
    assert user_liked_sites[1] == user_site_relationship1.to_uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_visited_sites(generate_user_site_relationship):
    user_uuid = uuid4()
    user_site_relationship1 = await generate_user_site_relationship(from_uuid=user_uuid, relationship="visited")
    user_site_relationship2 = await generate_user_site_relationship(from_uuid=user_uuid, relationship="visited")
    async with ro_async_session() as session:
        user_liked_sites = await user_site_api.get_user_visited_sites(session, user_uuid)

    assert len(user_liked_sites) == 2
    assert user_liked_sites[0] == user_site_relationship2.to_uuid
    assert user_liked_sites[1] == user_site_relationship1.to_uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_user_site_relationship():
    user_uuid = uuid4()
    site_uuid = uuid4()
    user_site_relationship_view = UserSiteRelationshipView(
        uuid=uuid4(),
        from_uuid=user_uuid,
        to_uuid=site_uuid,
        relationship="like",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_user_site = await user_site_api.insert_user_site_relationship(session, user_site_relationship_view)
        user_site_relationship = await user_site_api.get_user_site_relationship(
            session, inserted_user_site.from_uuid, inserted_user_site.to_uuid, "like"
        )

    assert user_site_relationship_view.uuid == user_site_relationship.uuid
