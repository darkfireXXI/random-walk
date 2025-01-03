from db.models.relationship import CategorySiteRelationship
from sqlalchemy import delete, select


async def get_category_site_relationship(session, category_uuid, site_uuid):
    stmt = select(CategorySiteRelationship).where(
        CategorySiteRelationship.from_uuid == category_uuid,
        CategorySiteRelationship.to_uuid == site_uuid,
    )
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def insert_category_site_relationship(session, category_site_relationship_view):
    category_site_relationship = CategorySiteRelationship(
        uuid=category_site_relationship_view.uuid,
        from_uuid=category_site_relationship_view.from_uuid,
        to_uuid=category_site_relationship_view.to_uuid,
        relationship=category_site_relationship_view.relationship,
        created_at=category_site_relationship_view.created_at,
        updated_at=category_site_relationship_view.updated_at,
    )
    session.add(category_site_relationship)
    return category_site_relationship


async def delete_category_site_relationship(session, category_site_relationship_uuid):
    stmt = delete(CategorySiteRelationship).where(CategorySiteRelationship.uuid == category_site_relationship_uuid)
    await session.execute(stmt)
