import os

import pandas as pd


def dump_append(df: pd.DataFrame, dump_path: str):
    file_exists = os.path.exists(dump_path)
    header = not file_exists
    df.to_csv(dump_path, header=header, index=False, mode="a")

    absolute_dump_path = os.path.join(os.getcwd(), dump_path)
    print(f"Saved {len(df)} rows in file: \'{absolute_dump_path}\'.")
