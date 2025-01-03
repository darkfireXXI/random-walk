from dao import user_category_relationship as user_category_dao
from dao import user_site_relationship as user_site_dao
from db.models.main import Site
from db.models.relationship import CategorySiteRelationship
from sqlalchemy import or_, select


async def random_walk_up(session, user_uuid, limit=10):
    user_liked_categories = await user_category_dao.get_user_liked_categories(session, user_uuid)
    user_visited_sites = await user_site_dao.get_user_visited_sites(session, user_uuid)

    stmt = (
        (
            select(Site)
            .join(CategorySiteRelationship, Site.uuid == CategorySiteRelationship.to_uuid)
            .where(
                CategorySiteRelationship.from_uuid.in_(user_liked_categories),
                Site.uuid.notin_(user_visited_sites),
                or_(Site.status != "broken", Site.status.is_(None)),
            )
        )
        .distinct()
        .order_by(Site.score.desc())
        .limit(limit)
    )

    results = await session.execute(stmt)
    return results.scalars().all()


async def random_walk_down(session, user_uuid, limit=10):
    user_liked_categories = await user_category_dao.get_user_liked_categories(session, user_uuid)
    user_visited_sites = await user_site_dao.get_user_visited_sites(session, user_uuid)

    stmt = (
        (
            select(Site)
            .join(CategorySiteRelationship, Site.uuid == CategorySiteRelationship.to_uuid)
            .where(
                CategorySiteRelationship.from_uuid.in_(user_liked_categories),
                Site.uuid.notin_(user_visited_sites),
                or_(Site.status != "broken", Site.status.is_(None)),
            )
        )
        .distinct()
        .order_by(Site.score.asc())
        .limit(limit)
    )

    results = await session.execute(stmt)
    return results.scalars().all()
