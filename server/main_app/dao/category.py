from db.models.main import Category
from sqlalchemy import delete, select


async def get_category_by_uuid(session, category_uuid):
    stmt = select(Category).where(Category.uuid == category_uuid)
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def get_categories_by_uuids(session, category_uuids):
    stmt = select(Category).where(Category.uuid.in_(category_uuids))
    results = await session.execute(stmt)
    return results.scalars().all()


async def get_category_by_name(session, category_name):
    stmt = select(Category).where(Category.name == category_name)
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def get_categories_by_parent(session, parent_uuid):
    stmt = select(Category).where(Category.parent_uuid == parent_uuid).order_by(Category.name.asc())
    results = await session.execute(stmt)
    return results.scalars().all()


async def get_category_uuids_by_parent(session, parent_uuid):
    stmt = select(Category.uuid).where(Category.parent_uuid == parent_uuid).order_by(Category.name.asc())
    results = await session.execute(stmt)
    return results.scalars().all()


async def insert_category(session, category_view):
    category = Category(
        uuid=category_view.uuid,
        parent_uuid=category_view.parent_uuid,
        parent_name=category_view.parent_name,
        name=category_view.name,
        status=category_view.status,
        created_at=category_view.created_at,
        updated_at=category_view.updated_at,
    )
    session.add(category)
    return category


async def delete_category(session, category_uuid):
    stmt = delete(Category).where(Category.uuid == category_uuid)
    await session.execute(stmt)
