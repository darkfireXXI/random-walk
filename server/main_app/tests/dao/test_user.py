from uuid import uuid4

import pytest
from dao import user as user_dao
from db.utils import rw_async_session
from utils.utils import naive_utcnow
from views.main import UserView


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_insert_user():
    user_view = UserView(
        uuid=uuid4(),
        user_name="drip___drop",
        email="nah@hellyeah.com",
        password="passw0rd",
        photo=None,
        role="default",
        joined_at=naive_utcnow(),
        last_login=naive_utcnow(),
    )
    async with rw_async_session() as session, session.begin():
        inserted_user = await user_dao.insert_user(session, user_view)
        user = await user_dao.get_user_by_uuid(session, inserted_user.uuid)

    assert user_view.uuid == user.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_user_name(generate_user):
    inserted_user = await generate_user()
    async with rw_async_session() as session, session.begin():
        user = await user_dao.get_user_by_user_name(session, inserted_user.user_name)

    assert inserted_user.uuid == user.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_is_user_name_available(generate_user):
    user = await generate_user()
    async with rw_async_session() as session, session.begin():
        not_available = await user_dao.is_user_name_available(session, user.user_name)
        is_available = await user_dao.is_user_name_available(session, "bleep_bloop")

    assert not_available is False
    assert is_available is True


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user(generate_user):
    user = await generate_user()
    async with rw_async_session() as session, session.begin():
        await user_dao.delete_user(session, user.uuid)
        user = await user_dao.get_user_by_uuid(session, user.uuid)

    assert user is None
