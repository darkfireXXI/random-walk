from dataclasses import asdict

from api import random_walk as random_walk_api
from db.utils import ro_async_session
from utils.utils import custom_dict_factory


async def random_walk(user_uuid):
    async with ro_async_session() as session:
        sites = random_walk_api.random_walk(session, user_uuid)

    sites = [asdict(site, dict_factory=custom_dict_factory) for site in sites]
    return sites
