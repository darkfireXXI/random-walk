from db.models.main import Site
from sqlalchemy import delete, select


async def get_site_by_uuid(session, site_uuid):
    stmt = select(Site).where(Site.uuid == site_uuid)
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def get_sites_by_uuids(session, site_uuids):
    stmt = select(Site).where(Site.uuid.in_(site_uuids))
    results = await session.execute(stmt)
    return results.scalars().all()


async def insert_site(session, site_view):
    site = Site(
        uuid=site_view.uuid,
        url=site_view.url,
        name=site_view.name,
        status=site_view.status,
        likes=site_view.likes,
        dislikes=site_view.dislikes,
        collections=site_view.collections,
        score=site_view.score,
        thumbnail=site_view.thumbnail,
        submitted_by=site_view.submitted_by,
        created_at=site_view.created_at,
        updated_at=site_view.updated_at,
    )
    session.add(site)
    return site


async def delete_site(session, site_uuid):
    stmt = delete(Site).where(Site.uuid == site_uuid)
    await session.execute(stmt)
