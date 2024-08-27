from typing import Any

from src.database import execute, fetch_all, fetch_one, table_file_status
from src.exceptions import InvalidFileIdError


async def add_file(filename: str) -> dict[str, Any] | None:
    """
    Add file in db
    :param filename:
    :return: tuple(row inserted, status)
    """

    inset_query = (
        table_file_status.insert()
        .values(
            {
                "filename": filename,
            }
        )
        .returning(table_file_status)
    )

    return await fetch_one(inset_query)


async def update_row(filename: str, rows: int) -> dict[str, Any] | None:
    """
    Update row count
    :param filename:
    :param rows: rows
    :return: tuple(row inserted, status)
    """

    file = await get_file_by_name(filename)
    if not file:
        raise InvalidFileIdError()

    update_query = (
        table_file_status.update()
        .values(
            {
                "row": rows,
            }
        )
        .where(table_file_status.c.filename == filename)
        .returning(table_file_status)
    )

    return await fetch_one(update_query)


async def update_file_status(file_id: int, status: bool) -> dict[str, Any] | None:
    """
    Update file status
    :param file_id:
    :param status:
    :return: tuple(row inserted, status)
    """

    file = await get_file_by_id(file_id)
    if not file:
        raise InvalidFileIdError()

    update_query = (
        table_file_status.update()
        .values(
            {
                "is_active": status,
            }
        )
        .where(table_file_status.c.id == file_id)
        .returning(table_file_status)
    )
    return await fetch_one(update_query)


async def delete_file(file_id: int) -> None:
    """
    Delete file
    :param file_id:
    :return: tuple(row inserted, status)
    """

    file = await get_file_by_id(file_id)
    if not file:
        raise InvalidFileIdError()

    delete_query = (table_file_status.delete()).where(table_file_status.c.id == file_id)

    return await execute(delete_query)


async def get_file_by_id(file_id: int) -> dict[str, Any] | None:
    select_query = table_file_status.select().where(table_file_status.c.id == file_id)
    return await fetch_one(select_query)


async def get_file_by_name(filename: str) -> dict[str, Any] | None:
    select_query = table_file_status.select().where(
        table_file_status.c.filename == filename
    )
    return await fetch_one(select_query)


async def get_all_files() -> list[dict[str, Any]] | None:
    select_query = table_file_status.select().order_by(
        table_file_status.c.created_at.desc()
    )
    return await fetch_all(select_query)
