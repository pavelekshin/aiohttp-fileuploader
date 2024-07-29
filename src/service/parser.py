import itertools
from asyncio.log import logger
from pathlib import Path
from typing import Any

import pandas as pd
from pandas import DataFrame

from src import database
from src.constants import Tables
from src.exceptions import FileError, FileStructureError
from src.settings import settings


async def file_to_db(filename: str, filepath: Path) -> dict[str, Any]:
    """
    Handler for save file into db
    :param filename: filename
    :param filepath: filepath
    :return: dict {"rows": count, "status": success or error}
    """
    suffix = filename.split(".")[-1]
    match suffix:
        case "xlsx" | "xls":
            value, status = await xlsx_to_db(filepath)
        case "csv":
            value, status = await csv_to_db(filepath)
        case _:
            raise FileError(f"Provided filetype={suffix} not supported!")
    return {
        "rows": value,
        "status": "success" if not status else status,
    }


async def xlsx_to_db(filepath: Path) -> tuple[int, str | None]:
    """
    Excel file handler
    :param filepath: filepath
    :return: tuple(row,status)
    """
    with pd.ExcelFile(filepath) as xls:
        df = pd.read_excel(xls, sheet_name=None)
        for _page, row in df.items():
            row.rename(columns=str.lower, inplace=True)  # noqa
            header = row.columns.values.tolist()
            match sorted(header):
                case Tables.LS_PHONE.value:
                    value, status = await table_phone_ls(row)
                case _:
                    raise FileStructureError(f"Unsupported file structure {header}")
    return value, status


async def csv_to_db(filepath: Path) -> tuple[int, str | None]:
    """
    CSV file handler
    :param filepath: filepath
    :return: tuple(row,status)
    """
    value = 0
    with pd.read_csv(
        filepath, iterator=True, chunksize=settings.CHUNK_FILE_READ, sep=";"
    ) as csv_reader:
        for chunk in csv_reader:
            chunk.rename(columns=str.lower, inplace=True)
            header = chunk.columns.values.tolist()
            match sorted(header):
                case Tables.LS_PHONE.value:
                    row, status = await table_phone_ls(chunk)
                case Tables.ENT_SURVEY.value:
                    row, status = await table_ent_survey(chunk)
                case Tables.GEO.value:
                    row, status = await table_geo(chunk)
                case _:
                    raise FileStructureError(f"Unsupported file structure {header}")
            if status:
                break
            value += row
    return value, status


async def table_phone_ls(row: DataFrame) -> tuple[int, str | None]:
    """
    Table LS_Phone executed
    :param row: row to save
    :return: tuple(row inserted, status)
    """
    error = None
    df = row.dropna()
    value = df.astype({"phone_number": "str", "ls": "str"})
    if not value.empty:
        for chunk in itertools.batched(
            value.to_dict(orient="records"), settings.CHUNK_DB_WRITE
        ):
            try:
                await database.insert_many(
                    database.table_enterprise_survey.insert(), chunk
                )
            except ConnectionRefusedError as ex:
                error = f"DB connection issue {ex}"
                logger.exception(ex)
    return len(value) if not value.empty else 0, error


async def table_ent_survey(row: DataFrame) -> tuple[int, str | None]:
    """
    Table ent_survey executed
    :param row: row to save
    :return: tuple(row inserted, status)
    """
    error = None
    df = row.dropna()
    value = df.astype({"year": "int", "value": "str"})
    if not value.empty:
        for chunk in itertools.batched(
            value.to_dict(orient="records"), settings.CHUNK_DB_WRITE
        ):
            try:
                await database.insert_many(
                    database.table_enterprise_survey.insert(), chunk
                )
            except ConnectionRefusedError as ex:
                error = f"DB connection issue {ex}"
                logger.exception(ex)
    return len(value) if not value.empty else 0, error


async def table_geo(row: DataFrame) -> tuple[int, str | None]:
    """
    Table geo executed
    :param row: row to save
    :return: tuple(row inserted, status)
    """
    error = None
    df = row.dropna()
    value = df.astype({"year": "int", "ec_count": "int", "geo_count": "int"})
    if not value.empty:
        for chunk in itertools.batched(
            value.to_dict(orient="records"), settings.CHUNK_DB_WRITE
        ):
            try:
                await database.insert_many(database.table_geo.insert(), chunk)
            except ConnectionRefusedError as ex:
                error = f"DB connection issue {ex}"
                logger.exception(ex)
    return len(value) if not value.empty else 0, error
