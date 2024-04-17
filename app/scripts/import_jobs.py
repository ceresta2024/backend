from datetime import datetime

import pandas as pd

from app.models.base import engine
from app.models.user import Job, Skill
from app.models.notice import Notice
from sqlalchemy.dialects.postgresql import insert


FILE_PATH = "app/scripts/data/jobs.xlsx"

### Jobs Sheet
COLUMN_JOB_NO = "No"
COLUMN_JOB_NAME = "Job Name"
COLUMN_JOB_DESC = "Job Description"
COLUMN_JOB_GOLD = "Allowed Gold"
COLUMN_JOB_SPEED = "Speed"
MAP_JOB_COLUMNS = {
    COLUMN_JOB_NO: "id",
    COLUMN_JOB_NAME: "name",
    COLUMN_JOB_DESC: "description",
    COLUMN_JOB_GOLD: "allow_gold",
    COLUMN_JOB_SPEED: "speed",
}
VALIDATION_JOB_COLUMNS = [COLUMN_JOB_NAME]
REMOVAL_JOB_COLUMNS = []
JOB_NAMES = {
    # "miner": 1,
}

### Skills Sheet
COLUMN_SKILL_NO = "No"
COLUMN_SKILL_NAME = "Skill Name"
COLUMN_SKILL_ATTRIBUTES = "Skill Attributes"
COLUMN_SKILL_JOB_NAME = "Job Name"
COLUMN_SKILL_DESC = "Skill Description"
MAP_SKILL_COLUMNS = {
    COLUMN_SKILL_NO: "id",
    COLUMN_SKILL_NAME: "name",
    COLUMN_SKILL_ATTRIBUTES: "attributes",
    COLUMN_SKILL_JOB_NAME: "job_id",
}
VALIDATION_SKILL_COLUMNS = []
REMOVAL_SKILL_COLUMNS = [COLUMN_SKILL_DESC]
UPDATE_SKILL_COLUMNS = {
    COLUMN_SKILL_JOB_NAME: JOB_NAMES,
}

### Notifications Sheet
COLUMN_NOTICE_NO = "No"
COLUMN_NOTICE_CONTENTS = "Contents"
COLUMN_NOTICE_TYPE = "Type"
COLUMN_NOTICE_AVAILABLE = "Is Available"
MAP_NOTICE_COLUMNS = {
    COLUMN_NOTICE_NO: "id",
    COLUMN_NOTICE_CONTENTS: "contents",
    COLUMN_NOTICE_TYPE: "type",
    COLUMN_NOTICE_AVAILABLE: "is_available",
}
VALIDATION_NOTICE_COLUMNS = []
REMOVAL_NOTICE_COLUMNS = []
NOTICE_TYPES = {
    "event": 0,
    "item": 1,
}
NOTICE_AVAILABLES = {
    "no": 0,
    "yes": 1,
}
UPDATE_NOTICE_COLUMNS = {
    COLUMN_NOTICE_TYPE: NOTICE_TYPES,
    COLUMN_NOTICE_AVAILABLE: NOTICE_AVAILABLES,
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


def validate_sheet_data(df, VALIDATION_COLUMNS, REMOVAL_COLUMNS):
    df.columns = df.columns.str.strip()

    # remove invalid items
    df = df.dropna(subset=VALIDATION_COLUMNS)

    # remove unmatched columns to db
    for column in REMOVAL_COLUMNS:
        df.drop(column, inplace=True, axis="columns")

    return df


def import_excel_data(df, tablename, MAP_COLUMNS, UPDATE_COLUMNS={}):

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
        # Item.__tablename__,
        tablename,
        con=engine,
        if_exists="append",
        index=False,
        method=insert_on_duplicate,
    )


def populate_job_data():
    global JOB_NAMES, UPDATE_SKILL_COLUMNS

    # Read Excel file with multiple sheets
    xls = pd.read_excel(FILE_PATH, sheet_name=["jobs", "skills", "notices"])

    # Access individual sheets using sheet names
    df_jobs = xls["jobs"]
    df_skills = xls["skills"]
    df_notices = xls["notices"]

    ### import jobs
    df_jobs = validate_sheet_data(df_jobs, VALIDATION_JOB_COLUMNS, REMOVAL_JOB_COLUMNS)
    JOB_NAMES = dict(
        zip(df_jobs[COLUMN_JOB_NAME], range(1, len(df_jobs[COLUMN_JOB_NAME]) + 1))
    )
    import_excel_data(df_jobs, Job.__tablename__, MAP_JOB_COLUMNS)

    ### import skills
    df_skills = validate_sheet_data(
        df_skills, VALIDATION_SKILL_COLUMNS, REMOVAL_SKILL_COLUMNS
    )
    UPDATE_SKILL_COLUMNS[COLUMN_SKILL_JOB_NAME] = JOB_NAMES
    import_excel_data(
        df_skills, Skill.__tablename__, MAP_SKILL_COLUMNS, UPDATE_SKILL_COLUMNS
    )

    ### import notices
    df_notices = validate_sheet_data(
        df_notices, VALIDATION_NOTICE_COLUMNS, REMOVAL_NOTICE_COLUMNS
    )
    import_excel_data(
        df_notices, Notice.__tablename__, MAP_NOTICE_COLUMNS, UPDATE_NOTICE_COLUMNS
    )

    return JOB_NAMES
