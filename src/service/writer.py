import asyncio
from asyncio import Task

from aiofile import async_open
from aiohttp import BodyPartReader, MultipartReader

from src.data.data_folder import get_data_path
from src.service import parser

CHUNK_SIZE = 8192


async def save_file_to_disk(
    part: MultipartReader | BodyPartReader | None, filename: str
) -> Task:
    """
    Save file on disk
    :param part: MultipartReader | BodyPartReader | None
    :param filename: filename
    :return: Task
    """
    size = 0
    filepath = get_data_path(filename)
    async with async_open(filepath, "wb") as af:
        while True:
            chunk = await part.read_chunk(size=CHUNK_SIZE)  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            await af.write(chunk)
    task = asyncio.create_task(
        parser.file_to_db(filename, filepath), name=f"Task-{filename}"
    )
    return task
