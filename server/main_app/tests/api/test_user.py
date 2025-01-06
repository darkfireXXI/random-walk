from uuid import uuid4

import pytest
from api import user as user_api
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
        inserted_user = await user_api.upsert_user(session, user_view)
        user = await user_api.get_user_by_uuid(session, inserted_user.uuid)

    assert user_view.uuid == user.uuid


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_update_user():
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
        await user_api.upsert_user(session, user_view)

    user_view.user_name = "new_name"
    user_view.email = "new@mail.com"
    user_view.photo = "photo.url"
    user_view.role = "moderator"
    async with rw_async_session() as session, session.begin():
        updated_user = await user_api.upsert_user(session, user_view)
        user = await user_api.get_user_by_uuid(session, updated_user.uuid)

    assert user_view.uuid == user.uuid
    assert user.user_name == "new_name"
    assert user.email == "new@mail.com"
    assert user.photo == "photo.url"
    assert user.role == "moderator"
