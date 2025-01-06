from uuid import uuid4

import pytest
from api import category_group as category_group_api
from db.utils import ro_async_session, rw_async_session
from utils.utils import naive_utcnow
from views.main import CategoryGroupView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_category_groups(generate_category_group):
    await generate_category_group(name="cool1")
    await generate_category_group(name="cool2")
    await generate_category_group(name="cool3")
    async with ro_async_session() as session:
        category_groups = await category_group_api.get_all_category_groups(session)

    assert len(category_groups) == 3
    assert category_groups[0].name == "cool1"
    assert category_groups[1].name == "cool2"
    assert category_groups[2].name == "cool3"


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_category_group():
    category_group_view = CategoryGroupView(
        uuid=uuid4(),
        name="cool",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_category_group = await category_group_api.upsert_category_group(session, category_group_view)
        category_group = await category_group_api.get_category_group_by_uuid(session, inserted_category_group.uuid)

    assert category_group_view.uuid == category_group.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_update_category_group():
    category_group_view = CategoryGroupView(
        uuid=uuid4(),
        name="cool",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        await category_group_api.upsert_category_group(session, category_group_view)

    category_group_view.name = "cooler"
    async with rw_async_session() as session, session.begin():
        updated_category_group = await category_group_api.upsert_category_group(session, category_group_view)
        category_group = await category_group_api.get_category_group_by_uuid(session, updated_category_group.uuid)

    assert category_group_view.uuid == category_group.uuid
    assert category_group.name == "cooler"
