import os
import re

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text


def camel2snake(camel_str):
    snake = re.sub(r"([a-z0-9])([A-Z])", lambda x: f"{x.group(1)}_{x.group(2)}", camel_str)
    return snake.lower()


def generate_connection_address(sync=False):
    if sync:
        library = "psycopg2"
    else:
        library = "asyncpg"
    db_address = f"postgresql+{library}://admin_user:db_password@0.0.0.0:15432/postgres"
    db_address = os.getenv("DATABASE_URL", db_address)
    return db_address


rw_async_engine = create_async_engine(
    generate_connection_address(sync=False),
    future=True,
    pool_use_lifo=False,
    pool_pre_ping=True,
    pool_size=5,
    pool_timeout=15,
    max_overflow=0,
    connect_args={},
    echo=False,
)

ro_async_engine = create_async_engine(
    generate_connection_address(sync=False),
    future=True,
    pool_use_lifo=False,
    pool_pre_ping=True,
    pool_size=5,
    pool_timeout=15,
    max_overflow=0,
    connect_args={},
    echo=False,
)

rw_sync_engine = create_engine(
    generate_connection_address(sync=True),
    future=True,
    pool_use_lifo=False,
    pool_pre_ping=True,
    pool_size=5,
    pool_timeout=15,
    max_overflow=0,
    connect_args={},
    echo=False,
)

ro_sync_engine = create_engine(
    generate_connection_address(sync=True),
    future=True,
    pool_use_lifo=False,
    pool_pre_ping=True,
    pool_size=5,
    pool_timeout=15,
    max_overflow=0,
    connect_args={},
    echo=False,
)

rw_async_session = sessionmaker(bind=rw_async_engine, expire_on_commit=False, class_=AsyncSession)
ro_async_session = sessionmaker(bind=ro_async_engine, expire_on_commit=False, class_=AsyncSession)

rw_sync_session = sessionmaker(bind=rw_sync_engine, expire_on_commit=False, class_=Session)
ro_sync_session = sessionmaker(bind=ro_sync_engine, expire_on_commit=False, class_=Session)


async def init_database():
    async with rw_async_engine.connect() as connection:
        results = await connection.execute(text("SELECT 1"))
    print(results.all())
    async with rw_async_session() as session:
        results = await session.execute(text("SELECT 2"))
    print(results.all())
    with rw_sync_engine.connect() as connection:
        results = connection.execute(text("SELECT 3"))
    print(results.all())
    with rw_sync_session() as session:
        results = session.execute(text("SELECT 4"))
    print(results.all())
