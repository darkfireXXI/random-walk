from uuid import uuid4

import pytest
from dao import category as category_dao
from db.utils import rw_async_session
from utils.utils import naive_utcnow
from views.main import CategoryView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_category():
    category_view = CategoryView(
        uuid=uuid4(),
        name="cool stuff",
        parent_uuid=uuid4(),
        parent_name="cool",
        status=None,
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_category = await category_dao.insert_category(session, category_view)
        category = await category_dao.get_category_by_uuid(session, inserted_category.uuid)

    assert category_view.uuid == category.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category(generate_category):
    category = await generate_category()
    async with rw_async_session() as session, session.begin():
        await category_dao.delete_category(session, category.uuid)
        category = await category_dao.get_category_by_uuid(session, category.uuid)

    assert category is None
