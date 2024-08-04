from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    CursorResult,
    DateTime,
    Delete,
    ForeignKey,
    Identity,
    Insert,
    Integer,
    MetaData,
    Select,
    String,
    Table,
    Update,
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

table_file_status = Table(
    "uploaded_file",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("filename", String, nullable=False),
    Column("is_active", Boolean, server_default="t", default=True),
    Column("row", Integer, default=0),
    Column(
        "created_at",
        DateTime,
        server_default=func.date_trunc("second", func.now()),
        nullable=False,
    ),
    Column("updated_at", DateTime, onupdate=func.date_trunc("second", func.now())),
)

table_phone_ls = Table(
    "user_ls_phone",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("phone_number", String, nullable=False),
    Column("ls", String, nullable=False),
    Column("file_id", Integer, ForeignKey("uploaded_file.id"), nullable=False),
)

table_enterprise_survey = Table(
    "enterprise_survey",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("year", Integer),
    Column("industry_aggregation_nzsioc", String),
    Column("industry_code_nzsioc", String),
    Column("industry_name_nzsioc", String),
    Column("units", String),
    Column("variable_code", String),
    Column("variable_name", String),
    Column("variable_category", String),
    Column("value", String, nullable=True),
    Column("file_id", Integer, ForeignKey("uploaded_file.id"), nullable=False),
)

table_geo = Table(
    "geo",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("anzsic06", String, nullable=False),
    Column("area", String),
    Column("year", Integer, nullable=False),
    Column("geo_count", Integer, nullable=False),
    Column("ec_count", Integer, nullable=False),
    Column("file_id", Integer, ForeignKey("uploaded_file.id"), nullable=False),
)


async def fetch_one(query: Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        result = cursor.first()
        return result._asdict() if result else None


async def fetch_all(query: Select) -> list[dict[str, Any]]:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        return [r._asdict() for r in cursor.all()]


async def execute(query: Insert | Update | Delete) -> None:
    async with engine.begin() as conn:
        await conn.execute(query)


async def insert_many(query: Insert, value: list[dict]) -> None:
    async with engine.begin() as conn:
        await conn.execute(query, value)
