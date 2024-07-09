from typing import Any

from sqlalchemy import (
    Column,
    CursorResult,
    Delete,
    Identity,
    Insert,
    Integer,
    MetaData,
    Select,
    String,
    Table,
    Update,
)
from sqlalchemy.ext.asyncio import async_engine_from_config

from settings import db_settings, settings

DB_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

DATABASE_URL = str(settings.DATABASE_URL)

engine = async_engine_from_config(db_settings.config)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

auth_user = Table(
    "inset_table",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
)


async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        result = cursor.first()
        return result._asdict() if result else None


async def execute(select_query: Insert | Update | Delete) -> None:
    async with engine.begin() as conn:
        await conn.execute(select_query)
