from typing import Any

from src.db.db_folder import get_db_path


class SqlAlchemyConfig:
    """Base config, used for SQLAlchemy Engine."""

    __test__ = False

    DATABASE_URL: str = None  # type: ignore
    ECHO: bool = False
    ENGINE_OPTIONS: dict[str, Any] = {}

    @property
    def sa_database_uri(self) -> str:
        if self.__class__ is PostgreSQL or self.__class__ is SQLite:
            return self.DATABASE_URL
        else:
            raise NotImplementedError("This DB not implemented!")

    @property
    def sa_engine_options(self) -> dict[str, Any]:
        return self.ENGINE_OPTIONS

    @property
    def sa_echo(self) -> bool:
        return self.ECHO

    @property
    def config(self) -> dict[str, Any]:
        cfg = {"sqlalchemy.url": self.sa_database_uri, "sqlalchemy.echo": self.sa_echo}
        for k, v in self.sa_engine_options.items():
            cfg[f"sqlalchemy.{k}"] = v
        return cfg


class PostgreSQL(SqlAlchemyConfig):
    """Used for PostgresSQL database server."""

    ECHO: bool = False
    ENGINE_OPTIONS: dict[str, Any] = {
        "pool_size": 10,
        "pool_pre_ping": True,
    }

    def __init__(self, url: str, echo: bool | None = None) -> None:
        self.DATABASE_URL = url
        if echo:
            self.ECHO = echo


class SQLite(SqlAlchemyConfig):
    """Used for SQLite database server."""

    ECHO: bool = True
    DB_NAME: str = "webupload.sqlite"
    ENGINE_OPTIONS: dict[str, Any] = {
        "pool_pre_ping": True,
    }

    def __init__(self, db_name: str):
        if db_name.strip():
            self.DB_NAME = db_name
        self.DATABASE_URL = f"sqlite+aiosqlite:///{get_db_path(self.DB_NAME)}"
