from uuid import uuid4

import pytest
from dao import user_category_relationship as user_category_dao
from db.utils import rw_async_session
from utils.utils import naive_utcnow
from views.relationship import UserCategoryRelationshipView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_user_category_relationship():
    user_category_relationship_view = UserCategoryRelationshipView(
        uuid=uuid4(),
        from_uuid=uuid4(),
        to_uuid=uuid4(),
        relationship="like",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_category_site = await user_category_dao.insert_user_category_relationship(
            session, user_category_relationship_view
        )
        user_category_relationship = await user_category_dao.get_user_category_relationship(
            session,
            inserted_category_site.from_uuid,
            inserted_category_site.to_uuid,
        )

    assert user_category_relationship_view.uuid == user_category_relationship.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_liked_categories(generate_user_category_relationship):
    user_uuid = uuid4()
    user_category_relationship1 = await generate_user_category_relationship(from_uuid=user_uuid, relationship="like")
    await generate_user_category_relationship(from_uuid=user_uuid, relationship="idk_why_im_even_testing_this")
    async with rw_async_session() as session, session.begin():
        user_liked_categories = await user_category_dao.get_user_liked_categories(session, user_uuid)

    assert len(user_liked_categories) == 1
    assert user_liked_categories[0] == user_category_relationship1.to_uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user_category_relationship(generate_user_category_relationship):
    user_category_relationship = await generate_user_category_relationship()
    async with rw_async_session() as session, session.begin():
        await user_category_dao.delete_user_category_relationship(session, user_category_relationship.uuid)
        user_category_relationship = await user_category_dao.get_user_category_relationship(
            session,
            user_category_relationship.from_uuid,
            user_category_relationship.to_uuid,
        )

    assert user_category_relationship is None
