from datetime import datetime

import pandas as pd

from app.models.base import engine
from app.models.item import Item
from sqlalchemy.dialects.postgresql import insert


FILE_PATH = "app/scripts/items.xlsx"

COLUMN_NO = "No"
COLUMN_ITEM_NAME = "Item Name"
COLUMN_ITEM_GROUP = "Item Group"
COLUMN_FUNCTION = "Function"
COLUMN_ITEM_REFERENCE = "Item Reference"
COLUMN_ITEM_TYPE = "Item Type"
COLUMN_ITEM_LEVEL = "Item Level"
COLUMN_ATTRIBUTE = "Attribute"
COLUMN_STATUS = "Status"
COLUMN_GOLD = "Gold"
COLUMN_RESULT = "Result"

ITEM_FUNCTION_GOLD = 0
ITEM_FUNCTION_HEALTH_RECOVER = 1
ITEM_FUNCTION_ACCELERATE = 2
ITEM_FUNCTION_SPECIAL = 3
ITEM_FUNCTION_JOB = 4
ITEM_FUNCTIONS = {
    "Gold Item": ITEM_FUNCTION_GOLD,
    "Health Recover Item": ITEM_FUNCTION_HEALTH_RECOVER,
    "Accelerate Item": ITEM_FUNCTION_ACCELERATE,
    "Special Item": ITEM_FUNCTION_SPECIAL,
    "Job Item": ITEM_FUNCTION_JOB,
}

ITEM_TYPE_COMMON = 0
ITEM_TYPE_JOB = 1
ITEM_TYPE_EVENT = 2
ITEM_TYPE = {
    "Common": ITEM_TYPE_COMMON,
    "Job": ITEM_TYPE_JOB,
    "Event": ITEM_TYPE_EVENT,
}

ITEM_LEVEL_LOW = 0
ITEM_LEVEL_MEDIUM = 1
ITEM_LEVEL_HIGH = 2
ITEM_LEVEL = {
    "Low": ITEM_LEVEL_LOW,
    "Medium": ITEM_LEVEL_MEDIUM,
    "High": ITEM_LEVEL_HIGH,
}

UPDATE_COLUMNS = {
    COLUMN_FUNCTION: ITEM_FUNCTIONS,
    COLUMN_ITEM_TYPE: ITEM_TYPE,
    COLUMN_ITEM_LEVEL: ITEM_LEVEL,
}
VALIDATION_COLUMNS = [COLUMN_ITEM_NAME, COLUMN_GOLD]
REMOVAL_COLUMNS = [COLUMN_ITEM_REFERENCE, COLUMN_STATUS]

MAP_COLUMNS = {
    COLUMN_NO: "id",
    COLUMN_ITEM_NAME: "name",
    COLUMN_ITEM_GROUP: "group",
    COLUMN_FUNCTION: "function",
    COLUMN_ITEM_TYPE: "type",
    COLUMN_ITEM_LEVEL: "level",
    COLUMN_ATTRIBUTE: "description",
    COLUMN_GOLD: "price",
    COLUMN_RESULT: "img_path",
    # 'HP': 'hp',
    # 'SP': 'sp',
    # 'Duration': 'duration',
}


def insert_on_duplicate(table, conn, cols, data_iter):
    stmt = insert(table.table).values(list(data_iter))
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_={col: getattr(stmt.excluded, col) for col in cols if col not in ["created", "img_path"]},
    )
    conn.execute(stmt)


def populate_item_data():
    df = pd.read_excel(FILE_PATH)
    df.columns = df.columns.str.strip()

    # remove invalid items
    df = df.dropna(subset=VALIDATION_COLUMNS)
    df = df.drop(df[df.Status == "Working on it"].index)

    # remove unmatched columns to db
    for column in REMOVAL_COLUMNS:
        df.drop(column, inplace=True, axis="columns")

    # update item values
    for column, values in UPDATE_COLUMNS.items():
        for old, new in values.items():
            df.loc[df[column] == old, column] = new
    now = datetime.utcnow()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    df.insert(0, "created", date_time)
    df.insert(1, "updated", date_time)

    # Rename columns to db columns
    df = df.rename(columns=MAP_COLUMNS)

    # populate db
    df.to_sql(
        Item.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        method=insert_on_duplicate,
    )
