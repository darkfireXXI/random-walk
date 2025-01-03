from uuid import uuid4

import pytest
from dao import category_site_relationship as category_site_dao
from db.utils import rw_async_session
from utils.utils import naive_utcnow
from views.relationship import CategorySiteRelationshipView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_category_site_relationship():
    category_site_relationship_view = CategorySiteRelationshipView(
        uuid=uuid4(),
        from_uuid=uuid4(),
        to_uuid=uuid4(),
        relationship="tag",
        status=None,
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_category_site = await category_site_dao.insert_category_site_relationship(
            session, category_site_relationship_view
        )
        category_site_relationship = await category_site_dao.get_category_site_relationship(
            session,
            inserted_category_site.from_uuid,
            inserted_category_site.to_uuid,
        )

    assert category_site_relationship_view.uuid == category_site_relationship.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_site_relationship(generate_category_site_relationship):
    category_site_relationship = await generate_category_site_relationship()
    async with rw_async_session() as session, session.begin():
        await category_site_dao.delete_category_site_relationship(session, category_site_relationship.uuid)
        category_site_relationship = await category_site_dao.get_category_site_relationship(
            session,
            category_site_relationship.from_uuid,
            category_site_relationship.to_uuid,
        )

    assert category_site_relationship is None
