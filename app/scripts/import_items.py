from datetime import datetime

import pandas as pd

from sqlalchemy.dialects.postgresql import insert

from app.models.base import engine
from app.models.item import Item


FILE_PATH = "app/scripts/data/items.xlsx"

COLUMN_NO = "No"
COLUMN_ITEM_NAME = "Item Name"
COLUMN_ITEM_GROUP = "Item Group"
COLUMN_FUNCTION = "Function"
COLUMN_ITEM_REFERENCE = "Item Reference"
COLUMN_ITEM_TYPE = "Item Type"
COLUMN_JOB_TYPE = "Job Type"
COLUMN_ITEM_LEVEL = "Item Level"
COLUMN_ATTRIBUTE = "Attribute"
COLUMN_HP_EFFECT = "HP Effect"
COLUMN_SP_EFFECT = "SP Effect"
COLUMN_DURATION = "Duration"
COLUMN_STATUS = "Status"
COLUMN_GOLD = "Gold"
COLUMN_RESULT = "Result"
COLUMN_FEEDBACK = "Feedback"

ITEM_FUNCTION_GOLD = 0
ITEM_FUNCTION_HEALTH_RECOVER = 1
ITEM_FUNCTION_ACCELERATE = 2
ITEM_FUNCTION_SPECIAL = 3
ITEM_FUNCTION_JOB = 4
ITEM_FUNCTION_TRANSPORT_VEHICLE = 5
ITEM_FUNCTION_WEATHER = 6
ITEM_FUNCTIONS = {
    "Gold Item": ITEM_FUNCTION_GOLD,
    "Health Recover Item": ITEM_FUNCTION_HEALTH_RECOVER,
    "Accelerate Item": ITEM_FUNCTION_ACCELERATE,
    "Special Item": ITEM_FUNCTION_SPECIAL,
    "Job Item": ITEM_FUNCTION_JOB,
    "Transport Vehicle": ITEM_FUNCTION_TRANSPORT_VEHICLE,
    "Weather change item": ITEM_FUNCTION_WEATHER,
}

ITEM_TYPE_COMMON = 0
ITEM_TYPE_JOB = 1
ITEM_TYPE_JOB_REQUIREMENT = 2
ITEM_TYPE_EVENT = 3
ITEM_TYPE = {
    "Common": ITEM_TYPE_COMMON,
    "Job": ITEM_TYPE_JOB,
    "Job Requirement": ITEM_TYPE_JOB_REQUIREMENT,
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
VALIDATION_COLUMNS = [COLUMN_ITEM_NAME, COLUMN_GOLD, COLUMN_RESULT]
REMOVAL_COLUMNS = [COLUMN_ITEM_REFERENCE, COLUMN_STATUS, COLUMN_FEEDBACK]

MAP_COLUMNS = {
    COLUMN_NO: "id",
    COLUMN_ITEM_NAME: "name",
    COLUMN_ITEM_GROUP: "group",
    COLUMN_FUNCTION: "function",
    COLUMN_ITEM_TYPE: "type",
    COLUMN_JOB_TYPE: "job_id",
    COLUMN_ITEM_LEVEL: "level",
    COLUMN_ATTRIBUTE: "description",
    COLUMN_GOLD: "price",
    COLUMN_RESULT: "img_path",
    COLUMN_HP_EFFECT: "hp",
    COLUMN_SP_EFFECT: "sp",
    COLUMN_DURATION: "duration",
}


def insert_on_duplicate(table, conn, cols, data_iter):
    stmt = insert(table.table).values(list(data_iter))
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_={
            col: getattr(stmt.excluded, col)
            for col in cols
            if col not in ["created", "img_path"]
        },
    )
    conn.execute(stmt)


def populate_item_data(jobs):
    df = pd.read_excel(FILE_PATH)
    df.columns = df.columns.str.strip()

    # remove invalid items
    df = df.dropna(subset=VALIDATION_COLUMNS)
    df = df.drop(df[df.Status == "Working on it"].index)

    # remove unmatched columns to db
    for column in REMOVAL_COLUMNS:
        df.drop(column, inplace=True, axis="columns")

    # item_functions = set(df[COLUMN_FUNCTION].tolist())
    # print(item_functions)

    # update item values
    for column, values in UPDATE_COLUMNS.items():
        for old, new in values.items():
            df.loc[df[column] == old, column] = new
    for old, new in jobs.items():
        df.loc[df[COLUMN_JOB_TYPE] == old, COLUMN_JOB_TYPE] = new

    now = datetime.utcnow()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    df.insert(0, "created", date_time)
    df.insert(1, "updated", date_time)

    # Rename columns to db columns
    df = df.rename(columns=MAP_COLUMNS)

    # populate item db
    df.to_sql(
        Item.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        method=insert_on_duplicate,
    )

    return df
