"""Storage for postgres DB."""

import pandas as pd
from sqlalchemy import engine


def dump_append(
    df: pd.DataFrame, sql_table_name: str, engine: engine.Engine
) -> None:
    df.to_sql(name=sql_table_name, con=engine, if_exists="append", index=False)
