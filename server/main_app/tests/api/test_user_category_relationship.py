from uuid import uuid4

import pytest
from api import user_category_relationship as user_category_api
from db.utils import ro_async_session, rw_async_session
from utils.utils import naive_utcnow
from views.relationship import UserCategoryRelationshipView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_liked_categories(generate_user_category_relationship):
    user_uuid = uuid4()
    category1 = await generate_user_category_relationship(from_uuid=user_uuid)
    category2 = await generate_user_category_relationship(from_uuid=user_uuid)
    await generate_user_category_relationship(from_uuid=user_uuid, relationship="idk_why_im_even_testing_this")
    async with ro_async_session() as session:
        categories = await user_category_api.get_user_liked_categories(session, user_uuid)

    assert len(categories) == 2
    assert categories[0] == category1.to_uuid
    assert categories[1] == category2.to_uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_user_category_relationship():
    user_category_view = UserCategoryRelationshipView(
        uuid=uuid4(),
        from_uuid=uuid4(),
        to_uuid=uuid4(),
        relationship="like",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_user_category = await user_category_api.upsert_user_category_relationship(session, user_category_view)
        user_category_relationship = await user_category_api.get_user_category_relationship(
            session, inserted_user_category.from_uuid, inserted_user_category.to_uuid
        )

    assert user_category_view.uuid == user_category_relationship.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_update_user_category_relationship():
    user_category_view = UserCategoryRelationshipView(
        uuid=uuid4(),
        from_uuid=uuid4(),
        to_uuid=uuid4(),
        relationship="like",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        await user_category_api.upsert_user_category_relationship(session, user_category_view)

    user_category_view.relationship = "dislike"
    async with rw_async_session() as session, session.begin():
        updated_user_category = await user_category_api.upsert_user_category_relationship(session, user_category_view)
        user_category_relationship = await user_category_api.get_user_category_relationship(
            session, updated_user_category.from_uuid, updated_user_category.to_uuid
        )

    assert user_category_view.uuid == user_category_relationship.uuid
    assert user_category_relationship.relationship == "dislike"
