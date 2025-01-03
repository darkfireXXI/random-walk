from uuid import uuid4

import pytest
from dao import random_walk as random_walk_dao
from db.utils import ro_async_session


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_random_walk(
    generate_user_category_relationship,
    generate_category_site_relationship,
    generate_user_site_relationship,
    generate_site,
):
    user_uuid = uuid4()
    category_uuid1 = uuid4()
    category_uuid2 = uuid4()
    category_uuid3 = uuid4()
    category_uuid4 = uuid4()
    site_uuid1 = uuid4()
    site_uuid2 = uuid4()
    site_uuid3 = uuid4()
    site_uuid4 = uuid4()
    site_uuid5 = uuid4()

    # user likes 3 categories
    await generate_user_category_relationship(from_uuid=user_uuid, to_uuid=category_uuid1, relationship="like")
    await generate_user_category_relationship(from_uuid=user_uuid, to_uuid=category_uuid2, relationship="like")
    await generate_user_category_relationship(from_uuid=user_uuid, to_uuid=category_uuid3, relationship="like")

    # categories are tied to 4 sites
    # 2 categories are tagged to the same site, test getting distict sites
    # 1 category the user doesn't like is tagged to a website
    await generate_category_site_relationship(from_uuid=category_uuid1, to_uuid=site_uuid1, relationship="tag")
    await generate_category_site_relationship(from_uuid=category_uuid1, to_uuid=site_uuid2, relationship="tag")
    await generate_category_site_relationship(from_uuid=category_uuid2, to_uuid=site_uuid2, relationship="tag")
    await generate_category_site_relationship(from_uuid=category_uuid3, to_uuid=site_uuid3, relationship="tag")
    await generate_category_site_relationship(from_uuid=category_uuid3, to_uuid=site_uuid4, relationship="tag")
    await generate_category_site_relationship(from_uuid=category_uuid4, to_uuid=site_uuid5, relationship="tag")

    # user has already visited 1 site tagged to a category they
    await generate_user_site_relationship(from_uuid=user_uuid, to_uuid=site_uuid4, relationship="visited")

    # generate sites
    # sites 1 and 2 are the only ones that should return
    await generate_site(uuid=site_uuid1, url="www.coolest-site-ever1.com", score=5)
    await generate_site(uuid=site_uuid2, url="www.coolest-site-ever2.com", status="special", score=4)
    # site 3 is broken
    await generate_site(uuid=site_uuid3, url="www.coolest-site-ever3.com", status="broken")
    # site 4 is visited
    await generate_site(uuid=site_uuid4, url="www.coolest-site-ever4.com")
    # site 5 is tagged to a category the user doesn't like
    await generate_site(uuid=site_uuid5, url="www.coolest-site-ever5.com")

    async with ro_async_session() as session:
        best_sites = await random_walk_dao.random_walk_up(session, user_uuid)
        worst_sites = await random_walk_dao.random_walk_down(session, user_uuid)

    assert [site_uuid1, site_uuid2] == [site.uuid for site in best_sites]
    assert [site_uuid2, site_uuid1] == [site.uuid for site in worst_sites]
