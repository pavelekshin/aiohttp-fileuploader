from typing import Any


class SqlAlchemyConfig:
    """Base config, used for staging SQLAlchemy Engine."""

    __test__ = False

    DATABASE_URL: str = None
    ECHO: bool = False
    ENGINE_OPTIONS: dict[str, Any] = {}

    @property
    def sa_database_uri(self) -> str:
        if self.__class__ is PostgreSQL:
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
    """Uses for PostgresSQL database server."""

    ECHO: bool = False
    ENGINE_OPTIONS: dict[str, Any] = {
        "pool_size": 10,
        "pool_pre_ping": True,
    }

    def __init__(self, url):
        self.DATABASE_URL = url
