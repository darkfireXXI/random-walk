from dao import user as user_dao


async def get_user_by_uuid(session, user_uuid):
    user = await user_dao.get_user_by_uuid(session, user_uuid)
    return user.to_view()


async def get_user_by_user_name(session, user_name):
    user = await user_dao.get_user_by_user_name(session, user_name)
    return user.to_view()


async def is_user_name_available(session, user_name):
    user = await user_dao.is_user_name_available(session, user_name)
    return user.to_view()


async def upsert_user(session, user_view):
    user = await user_dao.get_user_by_uuid(session, user_view.uuid)
    if user:
        if user.user_name != user_view.user_name:
            if await user_dao.is_user_name_available(session, user_view.user_name):
                user.user_name = user_view.user_name
            else:
                raise Exception("Username not available")
        user.email = user_view.email
        user.password = user_view.password
        user.photo = user_view.photo
        user.role = user_view.role

    else:
        user = await user_dao.insert_user(session, user_view)

    return user.to_view()


async def delete_user(session, user_uuid):
    return await user_dao.delete_user(session, user_uuid)
