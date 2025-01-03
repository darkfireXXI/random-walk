import asyncio
from uuid import UUID, uuid4

from dao import user as user_dao
from db.models.main import Site, User
from db.utils import init_database, rw_async_session, rw_sync_session
from sqlalchemy.sql import text
from views.main import UserView

# from utils.utils import naive_utcnow
# from utils.utils import naive_utcnow

# init_database()
# asyncio.run(init_database())


async def test():
    # async with rw_async_session() as session:
    # 	# results = await session.execute(text("SELECT 1"))
    # 	results = await session.execute(text("SELECT * FROM user"))
    # 	# results = await session.execute(text("SELECT * FROM testing"))
    # 	# results = await session.execute(text("SELECT * FROM site"))
    # print(results.all())

    # from datetime import datetime, UTC

    # def naive_utcnow():
    # 	return datetime.now(UTC).replace(tzinfo=None)

    # user_view = User(
    # 	uuid=uuid4(),
    # 	user_name="drip___drop123",
    # 	email="nah@you-up.com",
    # 	password="passw0rd",
    # 	photo="",
    # 	joined_at=naive_utcnow(),
    # 	last_login=naive_utcnow(),
    # )
    # async with rw_async_session() as session, session.begin():
    # 	inserted_user = await user_dao.insert_user(session, user_view)
    # 	user = await user_dao.get_user_by_uuid(session, inserted_user.uuid)

    # async with rw_async_session() as session:
    # 	results = await session.execute(text("SELECT * FROM user"))
    # print(results.all())

    # async with rw_async_session() as session, session.begin():
    # 	await user_dao.delete_user(session, UUID('78af66a6-ec52-41d6-84e1-aaa93b107804'))

    async with rw_async_session() as session, session.begin():
        # 	users = await user_dao.get_users(session)
        # print(users)
        # results = await session.execute(text("SELECT * FROM user"))
        from sqlalchemy import select

        stmt = select(Site)
        results = await session.execute(stmt)
    users = results.scalars().all()
    print(users)
    print(len(users))
    for user in users:
        print(user.user_name)
    # print(list(results.scalars().all()))


# async def test2():
# 	with rw_sync_session() as session:
# 		results = await session.execute(text("SELECT 1"))
# 		# results = await session.execute(text("SELECT * FROM user"))
# 		# results = await session.execute(text("SELECT * FROM testing"))
# 	print(results.all())

asyncio.run(test())

# test2()
# asyncio.run(test2())


# insert_user
