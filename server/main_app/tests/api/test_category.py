from uuid import uuid4

import pytest
from api import category as category_api
from db.utils import ro_async_session, rw_async_session
from utils.utils import naive_utcnow
from views.main import CategoryView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_by_name(generate_category):
    inserted_category = await generate_category(name="cool stuff")
    async with ro_async_session() as session:
        category = await category_api.get_category_by_name(session, "cool stuff")

    assert category
    assert inserted_category.uuid == category.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories_by_parent(generate_category):
    parent_uuid = uuid4()
    await generate_category(name="cool1", parent_uuid=parent_uuid)
    await generate_category(name="cool2", parent_uuid=parent_uuid)

    async with ro_async_session() as session:
        categories = await category_api.get_categories_by_parent(session, parent_uuid)

    assert len(categories) == 2
    assert categories[0].parent_uuid == parent_uuid
    assert categories[1].parent_uuid == parent_uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_uuids_by_parent(generate_category):
    parent_uuid = uuid4()
    category1 = await generate_category(name="cool1", parent_uuid=parent_uuid)
    category2 = await generate_category(name="cool2", parent_uuid=parent_uuid)

    async with ro_async_session() as session:
        category_uuids = await category_api.get_category_uuids_by_parent(session, parent_uuid)

    assert len(category_uuids) == 2
    assert category_uuids[0] == category1.uuid
    assert category_uuids[1] == category2.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_cateogry():
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
        inserted_category = await category_api.upsert_category(session, category_view)
        category = await category_api.get_category_by_name(session, inserted_category.name)

    assert category_view.uuid == category.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_update_cateogry():
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
        await category_api.upsert_category(session, category_view)

    parent_uuid = uuid4()
    category_view.name = "cooler stuff"
    category_view.parent_uuid = parent_uuid
    category_view.parent_name = "not cool"
    category_view.status = "suggested"
    async with rw_async_session() as session, session.begin():
        upserted_category = await category_api.upsert_category(session, category_view)
        category = await category_api.get_category_by_name(session, upserted_category.name)

    assert category_view.uuid == category.uuid
    assert category.name == "cooler stuff"
    assert category.parent_uuid == parent_uuid
    assert category.parent_name == "not cool"
    assert category.status == "suggested"
