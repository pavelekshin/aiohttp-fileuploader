import pandas as pd
from pandas import DataFrame

from src import database


async def xlsx_to_db(file):
    with pd.ExcelFile(file) as xls:
        df = pd.read_excel(xls, sheet_name=None)
        for _page, row in df.items():
            match row.columns.values.tolist():
                case ["phone_number", "ls"]:
                    value = await user_phone_ls(row)
                case _:
                    raise Exception("Not valid data structure")
    return value


async def user_phone_ls(row):
    value: DataFrame | None = row.astype({"phone_number": "str", "ls": "str"})
    if not value.empty:
        await database.execute(
            database.user_phone_ls.insert(), value.to_dict(orient="records")
        )
    return len(value) if not value.empty else 0
