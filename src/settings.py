from dynaconf import Dynaconf

from src.config.config import PostgreSQL

settings = Dynaconf(
    envvar_prefix=False,
    load_dotenv=True,
)

db_settings = PostgreSQL(url=settings.DATABASE_URL, echo=True)
