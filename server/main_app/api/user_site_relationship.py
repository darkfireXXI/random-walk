from dao import user_site_relationship as user_site_dao


async def get_user_site_relationship(session, user_uuid, site_uuid, relationship):
    user_site_relationship = await user_site_dao.get_user_site_relationship(session, user_uuid, site_uuid, relationship)
    return user_site_relationship.to_view()


async def get_user_liked_sites(session, user_uuid):
    return await user_site_dao.get_user_liked_sites(session, user_uuid)


async def get_user_visited_sites(session, user_uuid):
    return await user_site_dao.get_user_visited_sites(session, user_uuid)


async def insert_user_site_relationship(session, user_category_relationship_view):
    user_site_relationship = await user_site_dao.insert_user_site_relationship(session, user_category_relationship_view)
    return user_site_relationship.to_view()


async def delete_user_site_relationship(session, user_site_relationship_uuid):
    return await user_site_dao.delete_user_site_relationship(session, user_site_relationship_uuid)
