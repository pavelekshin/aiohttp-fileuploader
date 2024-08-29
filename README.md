# Aiohttp file uploader

- AioHTTP
- SQLAlchemy with slightly configured `alembic`
    - async SQLAlchemy engine
    - migrations set in easy to understand format (`YYYY-MM-DD_HHmm_rev_slug`)
- [aiofile](https://pypi.org/project/aiofile/) for async IO file operations
- alembic for data model and migrations
- Pandas for read CSV/EXCEL (supported MIME types : csv, xls, xlsx)
- CSV delimiter is ";"
- UI for following basic operations: upload/delete/activate/deactivate uploaded files
- JavaScript vanilla uploader
- configurable file read (csv only) and db write chunk size
- custom exceptions with global exceptions handlers
- mypy type checked
- ruff linters / formater
- some data for play find at: https://www.stats.govt.nz/large-datasets/csv-files-for-download/
- tested on following
  datasets: [Geo data](https://www.stats.govt.nz/assets/Uploads/New-Zealand-business-demography-statistics/New-Zealand-business-demography-statistics-At-February-2023/Download-data/geographic-units-by-industry-and-statistical-area-20002023-descending-order-.zip
  ), [Research survey](https://www.stats.govt.nz/assets/Uploads/Research-and-development-survey/Research-and-development-survey-2023/Download-data/research-and-development-survey-2023.csv)

well-structured code:

```bash
.
├── README.md
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── docker-compose.yml
├── .env
├── requremenets.txt
├── pyproject.toml
└── src                                                          -- src
    ├── __init__.py
    ├── app.py
    ├── config                                                   -- config folder
    │   └── config.py
    ├── constants.py
    ├── data                                                     -- data folder
    │   ├── data_folder.py
    ├── database.py
    ├── db
    │   └── db_folder.py
    ├── modules                                                  -- user class folder
    │   └── mod.py
    ├── exception_handlers.py                                    
    ├── exceptions.py
    ├── main.py
    ├── routes.py                                                 
    ├── service                                                   -- services
    │   ├── db.py
    │   ├── parser.py
    │   └── writer.py
    ├── settings.py
    ├── static
    │   ├── js
    │   └── style
    └── templates
        └── index.html

```

## Local Development

### First Build Only

1. `cp .env.example .env`
2. `docker-compose up -d --build`

### Migrations

- Create an automatic migration from changes in `src/database.py`

```shell
alembic revision -m *migration name* --autogenerate
```

- Run migrations

```shell
alembic upgrade head
```

- Downgrade migrations

```shell
alembic downgrade -1  # or -2 or base or hash of the migration
```