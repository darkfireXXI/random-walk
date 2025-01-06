from dao import category as category_dao
from utils.utils import naive_utcnow


async def get_categories_by_uuids(session, category_uuids):
    categories = await category_dao.get_categories_by_uuids(session, category_uuids)
    categories = [category.to_view() for category in categories]
    return categories


async def get_category_by_name(session, category_name):
    category = await category_dao.get_category_by_name(session, category_name)
    return category.to_view()


async def get_categories_by_parent(session, parent_uuid):
    categories = await category_dao.get_categories_by_parent(session, parent_uuid)
    categories = [category.to_view() for category in categories]
    return categories


async def get_category_uuids_by_parent(session, parent_uuid):
    return await category_dao.get_category_uuids_by_parent(session, parent_uuid)


async def upsert_category(session, category_view):
    category = await category_dao.get_category_by_uuid(session, category_view.uuid)
    if category:
        category.parent_uuid = category_view.parent_uuid
        category.parent_name = category_view.parent_name
        category.name = category_view.name
        category.status = category_view.status
        category.updated_at = naive_utcnow()

    else:
        category = await category_dao.insert_category(session, category_view)

    return category.to_view()


async def delete_category(session, category_uuid):
    return await category_dao.delete_category(session, category_uuid)
