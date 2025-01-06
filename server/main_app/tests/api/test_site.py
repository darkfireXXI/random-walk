from uuid import uuid4

import pytest
from api import site as site_api
from db.utils import ro_async_session, rw_async_session
from utils.utils import naive_utcnow
from views.main import SiteView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_sites_by_uuids(generate_site):
    site1 = await generate_site(
        url="www.coolest-site-ever1.com",
    )
    site2 = await generate_site(
        url="www.coolest-site-ever2.com",
    )
    site_uuids = [site1.uuid, site2.uuid]
    async with ro_async_session() as session:
        sites = await site_api.get_sites_by_uuids(session, site_uuids)

    assert len(sites) == 2
    assert sites[0].uuid == site1.uuid
    assert sites[1].uuid == site2.uuid


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
        inserted_site = await site_api.upsert_site(session, site_view)
        site = await site_api.get_site_by_uuid(session, inserted_site.uuid)

    assert site_view.uuid == site.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_update_site():
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
        await site_api.upsert_site(session, site_view)

    submitted_by = uuid4()
    site_view.url = "new_url"
    site_view.name = "best site ever"
    site_view.status = "broken"
    site_view.likes = 3
    site_view.dislikes = 2
    site_view.collections = 1
    site_view.score = 0
    site_view.thumbnail = "pic.jpg"
    site_view.submitted_by = submitted_by
    async with rw_async_session() as session, session.begin():
        updated_site = await site_api.upsert_site(session, site_view)
        site = await site_api.get_site_by_uuid(session, updated_site.uuid)

    assert site_view.uuid == site.uuid
    assert site.url == "new_url"
    assert site.name == "best site ever"
    assert site.status == "broken"
    assert site.likes == 3
    assert site.dislikes == 2
    assert site.collections == 1
    assert site.score == 0
    assert site.thumbnail == "pic.jpg"
    assert site.submitted_by == submitted_by
