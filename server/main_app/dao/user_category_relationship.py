from db.models.relationship import UserCategoryRelationship
from sqlalchemy import delete, select


async def get_user_category_relationship(session, user_uuid, category_uuid):
    stmt = select(UserCategoryRelationship).where(
        UserCategoryRelationship.from_uuid == user_uuid,
        UserCategoryRelationship.to_uuid == category_uuid,
    )
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def get_user_liked_categories(session, user_uuid):
    stmt = select(UserCategoryRelationship.to_uuid).where(
        UserCategoryRelationship.from_uuid == user_uuid,
        UserCategoryRelationship.relationship == "like",
    )
    results = await session.execute(stmt)
    return results.scalars().all()


async def insert_user_category_relationship(session, user_category_relationship_view):
    user_category_relationship = UserCategoryRelationship(
        uuid=user_category_relationship_view.uuid,
        from_uuid=user_category_relationship_view.from_uuid,
        to_uuid=user_category_relationship_view.to_uuid,
        relationship=user_category_relationship_view.relationship,
        created_at=user_category_relationship_view.created_at,
        updated_at=user_category_relationship_view.updated_at,
    )
    session.add(user_category_relationship)
    return user_category_relationship


async def delete_user_category_relationship(session, user_category_relationship_uuid):
    stmt = delete(UserCategoryRelationship).where(UserCategoryRelationship.uuid == user_category_relationship_uuid)
    await session.execute(stmt)
