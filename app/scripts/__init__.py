from app.scripts.import_jobs import populate_job_data
from app.scripts.import_items import populate_item_data
from app.scripts.import_shop import populate_shop_data
from app.utils import JOBS


def populate_db():
    jobs = populate_job_data()
    JOBS["NAME_TO_ID"] = jobs
    JOBS["ID_TO_NAME"] = {value: key for key, value in jobs.items()}
    df = populate_item_data(jobs)
    populate_shop_data(df)
