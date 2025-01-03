from uuid import uuid4

import pytest
from dao import site as site_dao
from db.utils import rw_async_session
from utils.utils import naive_utcnow
from views.main import SiteView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_site():
    site_view = SiteView(
        uuid=uuid4(),
        url="www.coolest-site-ever.com",
        name=None,
        status=None,
        likes=0,
        dislikes=0,
        collections=0,
        score=0,
        thumbnail=None,
        submitted_by=None,
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_site = await site_dao.insert_site(session, site_view)
        site = await site_dao.get_site_by_uuid(session, inserted_site.uuid)

    assert site_view.uuid == site.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_sites_by_uuids(generate_site):
    site1 = await generate_site(url="www.coolest-site-ever1.com")
    site2 = await generate_site(url="www.coolest-site-ever2.com")
    site3 = await generate_site(url="www.coolest-site-ever3.com")
    site_uuids = [site1.uuid, site2.uuid, site3.uuid]
    async with rw_async_session() as session, session.begin():
        sites = await site_dao.get_sites_by_uuids(session, site_uuids)

    assert len(sites) == 3
    for i in range(len(site_uuids)):
        assert sites[i].uuid == site_uuids[i]


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_site(generate_site):
    site = await generate_site(url="www.coolest-site-ever1.com")
    async with rw_async_session() as session, session.begin():
        await site_dao.delete_site(session, site.uuid)
        site = await site_dao.get_site_by_uuid(session, site.uuid)

    assert site is None
