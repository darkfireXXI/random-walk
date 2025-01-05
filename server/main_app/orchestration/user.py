from dataclasses import asdict

from api import user as user_api
from db.utils import ro_async_session, rw_async_session
from utils.utils import custom_dict_factory


async def is_user_name_available(user_name):
    async with ro_async_session() as session:
        is_available = await user_api.is_user_name_available(session, user_name)

    return {"is_user_name_available": is_available}


async def upsert_user(user_view):
    if len(user_view.user_name) > 99:
        raise Exception("User name is too long")

    async with rw_async_session() as session, session.begin():
        user = await user_api.upsert_user(session, user_view)

    return asdict(user, dict_factory=custom_dict_factory)


async def login(email, password):
    async with ro_async_session() as session:
        user = await user_api.get_user_by_email_password(session, email, password)

    if user is None:
        raise Exception("Incorrect email or password")

    return asdict(user, dict_factory=custom_dict_factory)
