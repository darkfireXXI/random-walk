import random

from dao import random_walk as random_walk_dao


async def random_walk(session, user_uuid):
    best_sites = random_walk_dao.random_walk_up(session, user_uuid)
    worst_sites = random_walk_dao.random_walk_down(session, user_uuid)

    sites = best_sites + worst_sites
    random.shuffle(sites)

    sites = [site.to_view() for site in sites]
    return sites
