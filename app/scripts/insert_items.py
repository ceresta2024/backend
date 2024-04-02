import pandas as pd

from app.models.base import engine

FILE_PATH = "app/scripts/items.xlsx"


def populate_item_data():
    df = pd.read_excel(FILE_PATH)

    # remove all rows that status is on working
    df = df.drop(df[df.Status == 'Working on it'].index)

    # remove unmatched columns to db
    for column in ["Item Reference", "Status"]:
        df.drop(column, inplace=True, axis="columns")

    df.columns = df.columns.str.strip()
    print(df.columns)

    # df.to_sql(table_name, con=engine, if_exists="replace", index=False)
