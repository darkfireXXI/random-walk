from dao import category_group as category_group_dao
from utils.utils import naive_utcnow


async def get_category_group_by_uuid(session, category_group_uuid):
    category_group = await category_group_dao.get_category_group_by_uuid(session, category_group_uuid)
    return category_group.to_view()


async def get_all_category_groups(session):
    category_groups = await category_group_dao.get_all_category_groups(session)
    category_groups = [category_group.to_view() for category_group in category_groups]
    return category_groups


async def upsert_category_group(session, category_group_view):
    category_group = await category_group_dao.get_category_group_by_uuid(session, category_group_view.uuid)
    if category_group:
        category_group.name = category_group_view.name
        category_group.updated_at = naive_utcnow()

    else:
        category_group = await category_group_dao.insert_category_group(session, category_group_view)

    return category_group.to_view()


async def delete_category_group(session, category_group_uuid):
    return await category_group_dao.delete_category_group(session, category_group_uuid)
