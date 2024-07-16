import asyncio

import aiohttp
from aiohttp import web
from aiohttp.web_request import Request

from src.data.data_folder import get_data_folder
from src.service import parse_file
from src.settings import settings

CHUNK_SIZE = 8192
CONTENT_TYPE = settings.CONTENT_TYPE
MAX_FILE_SIZE = 1024 * 1024 * settings.MAX_FILE_SIZE  # 100MB


async def index(request: Request):
    return web.FileResponse("templates/index.html")


def setup_routes(app: web.Application):
    app.router.add_route("GET", "/upload", index)
    app.router.add_route("POST", "/upload", handle_file_upload)
    app.router.add_static("/static", "static")


background_tasks = set()


async def handle_file_upload(request: Request):
    reader = await request.multipart()
    if int(reader.headers[aiohttp.hdrs.CONTENT_LENGTH]) > MAX_FILE_SIZE:
        return web.Response(
            text="File to big",
            status=400,
        )
    while part := await reader.next():
        filename = part.filename
        if part.headers[aiohttp.hdrs.CONTENT_TYPE] not in CONTENT_TYPE:
            return web.Response(
                text=f"Wrong filetype is uploaded .{filename.split(".")[-1].upper()}",
                status=400,
            )
        # You cannot rely on Content-Length if transfer is chunked.
        size = 0
        save_file = get_data_folder(filename)
        with open(save_file, "wb") as f:
            while True:
                chunk = await part.read_chunk()  # 8192 bytes by default.
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
        task = asyncio.create_task(parse_file.xlsx_to_db(save_file))
        background_tasks.add(task)
        task.add_done_callback(background_tasks.remove)
    await asyncio.wait(background_tasks)
    return web.Response(text="Uploaded", status=200)
