from enum import Enum


class Tables(Enum):
    LS_PHONE = sorted(["ls", "phone_number"])
    ENT_SURVEY = sorted(
        [
            "year",
            "industry_aggregation_nzsioc",
            "industry_code_nzsioc",
            "industry_name_nzsioc",
            "units",
            "variable_code",
            "variable_name",
            "variable_category",
            "value",
        ]
    )
    GEO = sorted(["anzsic06", "area", "year", "geo_count", "ec_count"])


class ErrorCode:
    INTERNAL_SERVER_ERROR = "Internal Server error"
    FILE_ERROR = "File error"


class ErrorMessage:
    INTERNAL_SERVER_ERROR = "Internal Server error"
    INVALID_FILE_TYPE = "Invalid file type is provided"
    FILE_TO_BIG = "File size is to big"
    INVALID_FILE_STRUCTURE = "Invalid file structure"
