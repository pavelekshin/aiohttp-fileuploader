from typing import Any

from sqlalchemy import (
    Column,
    CursorResult,
    DateTime,
    Identity,
    Insert,
    Integer,
    MetaData,
    Select,
    String,
    Table,
    func,
)
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.settings import db_settings, settings

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

user_phone_ls = Table(
    "user_ls_phone",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("phone_number", String, nullable=False),
    Column("ls", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)


async def fetch_one(query: Select) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        result = cursor.first()
        return result._asdict() if result else None


async def execute(query: Insert, value: list[dict]) -> None:
    async with engine.begin() as conn:
        await conn.execute(query, value)
