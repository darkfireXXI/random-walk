from db.models.main import User
from sqlalchemy import delete, select


async def get_user_by_uuid(session, user_uuid):
    stmt = select(User).where(User.uuid == user_uuid)
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def get_user_by_user_name(session, user_name):
    stmt = select(User).where(User.user_name == user_name)
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def get_user_by_email_password(session, email, password):
    stmt = select(User).where(User.email == email, User.password == password)
    results = await session.execute(stmt)
    return results.scalars().one_or_none()


async def is_user_name_available(session, user_name):
    stmt = select(User.user_name).where(User.user_name == user_name)
    results = await session.execute(stmt)
    return not results.scalars().one_or_none()


async def insert_user(session, user_view):
    user = User(
        uuid=user_view.uuid,
        user_name=user_view.user_name,
        email=user_view.email,
        password=user_view.password,
        photo=user_view.photo,
        role=user_view.role,
        joined_at=user_view.joined_at,
        last_login=user_view.last_login,
    )
    session.add(user)
    return user


async def delete_user(session, user_uuid):
    stmt = delete(User).where(User.uuid == user_uuid)
    await session.execute(stmt)
