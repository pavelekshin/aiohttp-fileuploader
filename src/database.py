from sqlalchemy import (
    Column,
    DateTime,
    Delete,
    Identity,
    Insert,
    Integer,
    MetaData,
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

table_phone_ls = Table(
    "user_ls_phone",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("phone_number", String, nullable=False),
    Column("ls", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)

table_enterprise_survey = Table(
    "enterprise_survey",
    metadata,
    Column("year", Integer),
    Column("industry_aggregation_nzsioc", String),
    Column("industry_code_nzsioc", String),
    Column("industry_name_nzsioc", String),
    Column("units", String),
    Column("variable_code", String),
    Column("variable_name", String),
    Column("variable_category", String),
    Column("value", String, nullable=True),
)

table_geo = Table(
    "geo",
    metadata,
    Column("anzsic06", String, nullable=False),
    Column("area", String),
    Column("year", Integer, nullable=False),
    Column("geo_count", Integer, nullable=False),
    Column("ec_count", Integer, nullable=False),
)


async def execute(query: Insert | Update | Delete) -> None:
    async with engine.begin() as conn:
        await conn.execute(query)


async def insert_many(query: Insert, value: list[dict]) -> None:
    async with engine.begin() as conn:
        await conn.execute(query, value)
