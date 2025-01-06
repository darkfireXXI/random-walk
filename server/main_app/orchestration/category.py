from dataclasses import asdict
from uuid import uuid4

from api import category as category_api
from api import category_group as category_group_api
from api import user_category_relationship as user_category_api
from db.utils import ro_async_session, rw_async_session
from utils.utils import custom_dict_factory, naive_utcnow
from views.relationship import UserCategoryRelationshipView


async def list_all_category_groups():
    async with ro_async_session() as session:
        category_groups = await category_group_api.get_all_category_groups(session)

    category_groups = [asdict(cg, dict_factory=custom_dict_factory) for cg in category_groups]
    return category_groups


async def like_category_group(user_uuid, category_group_uuid):
    async with rw_async_session() as session, session.begin():
        category_uuids = await category_api.get_category_uuids_by_parent(session, category_group_uuid)
        for category_uuid in category_uuids:
            user_category_relationship_view = UserCategoryRelationshipView(
                uuid=uuid4(),
                from_uuid=user_uuid,
                to_uuid=category_uuid,
                relationship="like",
                created_at=naive_utcnow(),
                updated_at=naive_utcnow(),
            )
            await user_category_api.upsert_user_category_relationship(session, user_category_relationship_view)


async def dislike_category_group(user_uuid, category_group_uuid):
    async with rw_async_session() as session, session.begin():
        category_uuids = await category_api.get_category_uuids_by_parent(session, category_group_uuid)
        for category_uuid in category_uuids:
            await user_category_api.delete_user_category_relationship(session, user_uuid, category_uuid)


async def list_all_categories(category_group_uuid):
    async with ro_async_session() as session:
        categories = await category_api.get_categories_by_parent(session, category_group_uuid)

    categories = [asdict(category, dict_factory=custom_dict_factory) for category in categories]
    return categories


async def like_category(user_uuid, category_uuid):
    async with rw_async_session() as session, session.begin():
        user_category_relationship = await user_category_api.delete_user_category_relationship(
            session, user_uuid, category_uuid
        )
    return asdict(user_category_relationship, dict_factory=custom_dict_factory)


async def dislike_category(user_uuid, category_uuid):
    async with rw_async_session() as session, session.begin():
        return await user_category_api.delete_user_category_relationship(session, user_uuid, category_uuid)


async def get_user_liked_categories(user_uuid):
    async with ro_async_session() as session:
        category_uuids = await user_category_api.get_user_liked_categories(session, user_uuid)
        categories = category_api.get_categories_by_uuids(session, category_uuids)

    categories = [asdict(category, dict_factory=custom_dict_factory) for category in categories]
    return categories
