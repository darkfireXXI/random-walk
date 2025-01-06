from db.models.relationship import UserSiteRelationship
from sqlalchemy import delete, select


async def get_user_site_relationship(session, user_uuid, site_uuid, relationship):
    stmt = select(UserSiteRelationship).where(
        UserSiteRelationship.from_uuid == user_uuid,
        UserSiteRelationship.to_uuid == site_uuid,
        UserSiteRelationship.relationship == relationship,
    )
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def get_user_liked_sites(session, user_uuid):
    stmt = (
        select(UserSiteRelationship.to_uuid)
        .where(
            UserSiteRelationship.from_uuid == user_uuid,
            UserSiteRelationship.relationship == "like",
        )
        .order_by(UserSiteRelationship.updated_at.desc())
    )
    results = await session.execute(stmt)
    return results.scalars().all()


async def get_user_visited_sites(session, user_uuid):
    stmt = (
        select(UserSiteRelationship.to_uuid)
        .where(
            UserSiteRelationship.from_uuid == user_uuid,
            UserSiteRelationship.relationship == "visited",
        )
        .order_by(UserSiteRelationship.updated_at.desc())
    )
    results = await session.execute(stmt)
    return results.scalars().all()


async def insert_user_site_relationship(session, user_site_relationship_view):
    user_site_relationship = UserSiteRelationship(
        uuid=user_site_relationship_view.uuid,
        from_uuid=user_site_relationship_view.from_uuid,
        to_uuid=user_site_relationship_view.to_uuid,
        relationship=user_site_relationship_view.relationship,
        created_at=user_site_relationship_view.created_at,
        updated_at=user_site_relationship_view.updated_at,
    )
    session.add(user_site_relationship)
    return user_site_relationship


async def delete_user_site_relationship(session, user_site_relationship_uuid):
    stmt = delete(UserSiteRelationship).where(UserSiteRelationship.uuid == user_site_relationship_uuid)
    await session.execute(stmt)
