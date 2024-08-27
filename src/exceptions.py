from src.constants import ErrorCode, ErrorMessage


class DetailedError(Exception):
    error_message = ErrorMessage.INTERNAL_SERVER_ERROR
    error_code = ErrorCode.INTERNAL_SERVER_ERROR
    error_detail = None

    def __init__(self, detail: str | None = None) -> None:
        self.error_detail = detail


class FileError(DetailedError):
    error_code = ErrorCode.FILE_ERROR
    error_message = ErrorMessage.INVALID_FILE_TYPE


class InvalidFileIdError(DetailedError):
    error_code = ErrorCode.INVALID_FILE_ID


class FileSizeError(DetailedError):
    error_code = ErrorCode.FILE_ERROR
    error_message = ErrorMessage.FILE_TO_BIG


class FileStructureError(DetailedError):
    error_code = ErrorCode.FILE_ERROR
    error_message = ErrorMessage.INVALID_FILE_STRUCTURE
