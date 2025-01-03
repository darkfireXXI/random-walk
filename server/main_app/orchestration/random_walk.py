from api import random_walk as random_walk_api
from db.utils import ro_async_session


async def random_walk(user_uuid):
    async with ro_async_session() as session:
        sites = random_walk_api.random_walk(session, user_uuid)

    # sites = [ for site]
    # convert from view to dict here, maybe make method?
    return sites
