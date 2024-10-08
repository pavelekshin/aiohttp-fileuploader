from asyncio.log import logger
from typing import Any

from aiohttp import web
from aiohttp.typedefs import Handler, Middleware

from src.exception_handlers import (
    base_exception_handler,
    file_id_error_exception_handler,
    file_size_error_exception_handler,
    file_structure_error_exception_handler,
    file_type_error_exception_handler,
)
from src.routes import (
    handle_change_status_activate,
    handle_change_status_deactivate,
    handle_delete_files,
    handle_file_upload,
    handle_get_files,
    index,
)


async def init_app() -> web.Application:
    """
    Init application settings
    :return:
    """
    # Create webapp
    app = web.Application()
    # init webapp routes
    setup_routes(app)
    # init middlewares handlers
    setup_middlewares(app)
    return app


def create_error_middleware(overrides: dict[str | int, Any]) -> Middleware:
    """
    Custom middleware error handler
    :param overrides: dict with exception handlers
    :return:
    """

    @web.middleware
    async def error_middleware(
        request: web.Request, handler: Handler
    ) -> web.StreamResponse:
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request, ex)
            raise
        except Exception as ex:
            override = overrides.get(ex.__class__.__name__)
            if override:
                logger.exception("Error handling request")
                return await override(request, ex)
            logger.exception("Error handling request")
            return await base_exception_handler(500, ex)

    return error_middleware


def setup_routes(app: web.Application) -> None:
    app.router.add_routes(
        [
            web.get("/", index),
            web.get("/files", handle_get_files),
            web.post("/upload", handle_file_upload),
            web.post("/{id}/activate", handle_change_status_activate),
            web.post("/{id}/deactivate", handle_change_status_deactivate),
            web.post("/{id}/delete", handle_delete_files),
            web.static("/static", "static"),
        ]
    )


def setup_middlewares(app: web.Application) -> None:
    error_middleware = create_error_middleware(
        {
            "FileError": file_type_error_exception_handler,
            "FileSizeError": file_size_error_exception_handler,
            "FileStructureError": file_structure_error_exception_handler,
            "InvalidFileIdError": file_id_error_exception_handler,
        }
    )
    app.middlewares.append(error_middleware)
