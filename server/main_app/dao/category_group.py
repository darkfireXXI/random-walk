from db.models.main import CategoryGroup
from sqlalchemy import delete, select


async def get_category_group_by_uuid(session, category_group_uuid):
    stmt = select(CategoryGroup).where(CategoryGroup.uuid == category_group_uuid)
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def insert_category_group(session, category_group_view):
    category = CategoryGroup(
        uuid=category_group_view.uuid,
        name=category_group_view.name,
        created_at=category_group_view.created_at,
        updated_at=category_group_view.updated_at,
    )
    session.add(category)
    return category


async def delete_category_group(session, category_group_uuid):
    stmt = delete(CategoryGroup).where(CategoryGroup.uuid == category_group_uuid)
    await session.execute(stmt)
