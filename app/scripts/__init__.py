from app.scripts.import_jobs import populate_job_data
from app.scripts.import_items import populate_item_data
from app.scripts.import_shop import populate_shop_data


def populate_db():
    jobs = populate_job_data()
    df = populate_item_data(jobs)
    populate_shop_data(df)
