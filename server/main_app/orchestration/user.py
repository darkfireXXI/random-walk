from dataclasses import asdict

from api import user as user_api
from db.utils import rw_async_session
from utils.utils import custom_dict_factory


async def upsert_user(user_view):
    async with rw_async_session() as session, session.begin():
        user = await user_api.upsert_user(session, user_view)
        return asdict(user, dict_factory=custom_dict_factory)
