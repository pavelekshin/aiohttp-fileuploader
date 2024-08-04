import asyncio
from asyncio import Task

from aiofile import async_open
from aiohttp import BodyPartReader, MultipartReader

from src.modules.mod import File
from src.service import parser

CHUNK_SIZE = 8192


async def save_file_to_disk(
    part: MultipartReader | BodyPartReader | None, file: File
) -> Task:
    """
    Save file on disk
    :param part: MultipartReader | BodyPartReader | None
    :param file: File object
    :return: Task
    """
    size = 0
    async with async_open(file.filepath, "wb") as af:
        while True:
            chunk = await part.read_chunk(size=CHUNK_SIZE)  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            await af.write(chunk)
    print(file)
    task = asyncio.create_task(
        parser.file_to_db(file), name=f"Task-{file.saved_filename}"
    )
    return task
