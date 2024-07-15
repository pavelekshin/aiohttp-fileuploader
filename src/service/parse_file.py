import pandas as pd
from pandas import DataFrame

from src import database


async def xlsx_to_db(file):
    with pd.ExcelFile(file) as xls:
        df = pd.read_excel(xls, sheet_name=None,)
        for _page, row in df.items():
            value: DataFrame | None = (
                row.astype({"password": "str"})
                .fillna({"age": 0})
                .astype({"age": "int8"})
            )
            if not value.empty:
                await database.execute(
                    database.auth_user.insert(), value.to_dict(orient="records")
                )
    return len(value) if not value.empty else 0
