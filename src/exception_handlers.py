from aiohttp import web

from src.exceptions import (
    FileError,
    FileSizeError,
    FileStructureError,
    InvalidFileIdError,
)


async def file_type_error_exception_handler(
    request: web.Request, exception: FileError
) -> web.Response:
    """
    Returns a Response for FileError exception.
    Used for error middleware.
    :param request: request
    :param exception: exception
    :return: web.Response
    """
    return web.json_response(
        status=400,
        data={
            "error_code": exception.error_code,
            "error_message": exception.error_message,
            "detail": exception.error_detail,
        },
    )


async def file_size_error_exception_handler(
    request: web.Request, exception: FileSizeError
) -> web.Response:
    """
    Returns a Response for FileSizeError exception.
    Used for error middleware.
    :param request: request
    :param exception: exception
    :return: web.Response
    """
    return web.json_response(
        status=400,
        data={
            "error_code": exception.error_code,
            "error_message": exception.error_message,
            "detail": exception.error_detail,
        },
    )


async def file_structure_error_exception_handler(
    request: web.Request, exception: FileStructureError
) -> web.Response:
    """
    Returns a Response for FileStructureError exception.
    Used for error middleware.
    :param request: request
    :param exception: exception
    :return: web.Response
    """
    return web.json_response(
        status=400,
        data={
            "error_code": exception.error_code,
            "error_message": exception.error_message,
            "detail": exception.error_detail,
        },
    )


async def file_id_error_exception_handler(
    request: web.Request, exception: InvalidFileIdError
) -> web.Response:
    """
    Returns a Response for FileStructureError exception.
    Used for error middleware.
    :param request: request
    :param exception: exception
    :return: web.Response
    """
    return web.json_response(
        status=500,
        data={
            "error_code": exception.error_code,
            "error_message": exception.error_message,
            "detail": exception.error_detail,
        },
    )


async def base_exception_handler(
    status_code: int, exception: Exception
) -> web.Response:
    """
    Returns a Response for any unhandled exception.
    Used for error middleware.
    :param status_code: status_code
    :param exception: exception
    :return: web.Response
    """
    return web.json_response(
        status=status_code,
        data={
            "error_code": "Internal Server Error",
            "error_message": str(exception),
        },
    )
