from dao import site as site_dao
from utils.utils import naive_utcnow


async def get_site_by_uuid(session, site_uuid):
    site = await site_dao.get_site_by_uuid(session, site_uuid)
    return site.to_view()


async def get_sites_by_uuids(session, site_uuid):
    sites = await site_dao.get_sites_by_uuids(session, site_uuid)
    sites = [site.to_view() for site in sites]
    return sites


async def upsert_site(session, site_view):
    site = await site_dao.get_site_by_uuid(session, site_view.uuid)
    if site:
        site.url = site_view.url
        site.name = site_view.name
        site.status = site_view.status
        site.likes = site_view.likes
        site.dislikes = site_view.dislikes
        site.collections = site_view.collections
        site.score = site_view.score
        site.thumbnail = site_view.thumbnail
        site.submitted_by = site_view.submitted_by
        site.updated_at = naive_utcnow()

    else:
        site = await site_dao.insert_site(session, site_view)

    return site.to_view()


async def delete_site(session, site_uuid):
    return site_dao.delete_site(session, site_uuid)
