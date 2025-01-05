from uuid import uuid4

import pytest
from dao import category_group as category_group_dao
from db.utils import rw_async_session
from utils.utils import naive_utcnow
from views.main import CategoryGroupView


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
        inserted_category_group = await category_group_dao.insert_category_group(session, category_group_view)
        category_group = await category_group_dao.get_category_group_by_uuid(session, inserted_category_group.uuid)

    assert category_group_view.uuid == category_group.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_category_groups(generate_category_group):
    await generate_category_group(name="a")
    await generate_category_group(name="b")
    await generate_category_group(name="c")
    async with rw_async_session() as session, session.begin():
        category_groups = await category_group_dao.get_all_category_groups(session)

    assert len(category_groups) == 3
    assert category_groups[0].name == "a"
    assert category_groups[1].name == "b"
    assert category_groups[2].name == "c"


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_group(generate_category_group):
    category_group = await generate_category_group()
    async with rw_async_session() as session, session.begin():
        await category_group_dao.delete_category_group(session, category_group.uuid)
        category_group = await category_group_dao.get_category_group_by_uuid(session, category_group.uuid)

    assert category_group is None
