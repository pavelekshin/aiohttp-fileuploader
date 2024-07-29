import asyncio

import aiohttp
from aiohttp import web
from aiohttp.web_request import Request

from src.exceptions import FileError, FileSizeError
from src.service.writer import save_file_to_disk
from src.settings import settings

CONTENT_TYPE = settings.CONTENT_TYPE
MAX_FILE_SIZE = 1024 * 1024 * settings.MAX_FILE_SIZE  # 100MB


async def index(request: Request):
    """
    Handle /upload GET request
    :param request:
    :return:
    """
    return web.FileResponse("templates/index.html")


async def handle_file_upload(request: Request):
    """
    Handle /upload POST request with mulipart
    :param request:
    :return:
    """
    tasks, resp = [], []
    reader = await request.multipart()
    if int(reader.headers[aiohttp.hdrs.CONTENT_LENGTH]) > MAX_FILE_SIZE:
        raise FileSizeError("File to big")
    while part := await reader.next():
        filename = part.filename
        if part.headers[aiohttp.hdrs.CONTENT_TYPE] not in CONTENT_TYPE:
            raise FileError(
                f"Wrong filetype is uploaded .{filename.split(".")[-1].upper()}"
            )
        tasks.append(await save_file_to_disk(part, filename))
    done, _pending = await asyncio.wait(tasks, return_when="ALL_COMPLETED")
    for complete_task in done:
        filename = complete_task.get_name().removeprefix("Task-")  # noqa: E501, substring ip address from task name
        resp.append({"filename": filename, **complete_task.result()})
    return web.json_response(
        status=200 if all(d.get("status") == "success" for d in resp) else 500,
        data=resp,
    )
