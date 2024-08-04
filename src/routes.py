import asyncio
import datetime
import json

import aiohttp
from aiohttp import web
from aiohttp.web_request import Request

from src.exceptions import FileError, FileSizeError
from src.modules.mod import File
from src.service import db, writer
from src.settings import settings

CONTENT_TYPE = settings.CONTENT_TYPE
MAX_FILE_SIZE = 1024 * 1024 * settings.MAX_FILE_SIZE  # 150MB


def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


async def index(request) -> web.FileResponse:
    """
    Handle GET requests and provide html templates
    :param request:
    :return:
    """
    path = request.path
    return web.FileResponse(f"templates/{path}/index.html")


async def handle_file_upload(request: Request) -> web.json_response:
    """
    Handle /upload POST request with multipart
    :param request:
    :return:
    """
    tasks, resp = [], []
    reader = await request.multipart()
    if int(reader.headers[aiohttp.hdrs.CONTENT_LENGTH]) > MAX_FILE_SIZE:
        raise FileSizeError("File to big")
    while part := await reader.next():
        file = File(filename=part.filename)
        if part.headers[aiohttp.hdrs.CONTENT_TYPE] not in CONTENT_TYPE:
            raise FileError(f"Wrong filetype is uploaded .{file.suffix.upper()}")
        tasks.append(await writer.save_file_to_disk(part, file))
    done, _pending = await asyncio.wait(tasks, return_when="ALL_COMPLETED")
    for complete_task in done:
        filename = complete_task.get_name().removeprefix("Task-")
        resp.append({"filename": filename, **complete_task.result()})
    return web.json_response(
        status=200 if all(d.get("status") == "success" for d in resp) else 500,
        data=resp,
    )


async def handle_get_files(request: Request) -> web.json_response:
    """
    Get uploaded files list
    :param request:
    :return:
    """

    if files := await db.get_all_files():
        return web.json_response(
            status=200,
            data=files,
            dumps=lambda item: json.dumps(item, default=serialize_datetime),
        )
    return web.json_response(404)


async def handle_change_status_activate(request: Request) -> web.json_response:
    """
    Change file status
    :param request:
    :return:
    """
    if file_id := request.match_info["id"]:
        return web.json_response(
            status=200,
            data=file_id,
        )
    return web.json_response(404)


async def handle_change_status_deactivate(request: Request) -> web.json_response:
    """
    Change file status
    :param request:
    :return:
    """
    if file_id := request.match_info["id"]:
        return web.json_response(
            status=200,
            data=file_id,
        )
    return web.json_response(404)
