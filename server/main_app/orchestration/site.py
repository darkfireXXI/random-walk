from dataclasses import asdict
from uuid import uuid4

from api import site as site_api
from api import user_site_relationship as user_site_api
from db.utils import ro_async_session, rw_async_session
from utils.utils import custom_dict_factory, naive_utcnow
from views.relationship import UserSiteRelationshipView


async def visit_site(user_uuid, site_uuid):
    user_site_relationship_view = UserSiteRelationshipView(
        uuid=uuid4(),
        from_uuid=user_uuid,
        to_uuid=site_uuid,
        relationship="visited",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        user_site_relationship = await user_site_api.insert_user_site_relationship(session, user_site_relationship_view)

    return asdict(user_site_relationship, dict_factory=custom_dict_factory)


async def like_site(user_uuid, site_uuid):
    user_site_relationship_view = UserSiteRelationshipView(
        uuid=uuid4(),
        from_uuid=user_uuid,
        to_uuid=site_uuid,
        relationship="like",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        user_site_relationship = await user_site_api.insert_user_site_relationship(session, user_site_relationship_view)

    return asdict(user_site_relationship, dict_factory=custom_dict_factory)


async def dislike_site(user_uuid, site_uuid):
    async with rw_async_session() as session, session.begin():
        user_site_relationship = await user_site_api.get_user_site_relationship(session, user_uuid, site_uuid, "like")
        if user_site_relationship:
            return await user_site_api.delete_user_site_relationship(session, user_site_relationship.uuid)


async def get_user_liked_sites(user_uuid):
    async with ro_async_session() as session:
        site_uuids = await user_site_api.get_user_liked_sites(session, user_uuid)
        sites = await site_api.get_sites_by_uuids(session, site_uuids)

    sites = [asdict(site, dict_factory=custom_dict_factory) for site in sites]
    return sites


async def get_user_visited_sites(user_uuid):
    async with ro_async_session() as session:
        site_uuids = await user_site_api.get_user_visited_sites(session, user_uuid)
        sites = await site_api.get_sites_by_uuids(session, site_uuids)

    sites = [asdict(site, dict_factory=custom_dict_factory) for site in sites]
    return sites
