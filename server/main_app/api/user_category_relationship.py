from dao import user_category_relationship as user_category_dao
from utils.utils import naive_utcnow


async def get_user_category_relationship(session, user_uuid, category_uuid):
    user_category_relationship = await user_category_dao.get_user_category_relationship(
        session, user_uuid, category_uuid
    )
    return user_category_relationship.to_view()


async def get_user_liked_categories(session, user_uuid):
    return await user_category_dao.get_user_liked_categories(session, user_uuid)


async def upsert_user_category_relationship(session, user_category_relationship_view):
    user_uuid = user_category_relationship_view.from_uuid
    category_uuid = user_category_relationship_view.to_uuid
    user_category_relationship = await user_category_dao.get_user_category_relationship(
        session, user_uuid, category_uuid
    )
    if user_category_relationship:
        user_category_relationship.relationship = user_category_relationship_view.relationship
        user_category_relationship.updated_at = naive_utcnow()

    else:
        user_category_relationship = await user_category_dao.insert_user_category_relationship(
            session, user_category_relationship_view
        )

    return user_category_relationship


async def delete_user_category_relationship(session, user_uuid, category_uuid):
    user_category_relationship = user_category_dao.get_user_category_relationship(session, user_uuid, category_uuid)
    if user_category_relationship:
        return await user_category_dao.delete_user_category_relationship(session, user_category_relationship.uuid)
