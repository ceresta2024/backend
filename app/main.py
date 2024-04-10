# main.py

from fastapi import FastAPI
from app.config import settings
from app.routes import router
from app.sockets import sio_app
from app.scripts.insert_items import populate_item_data
from app.scripts.import_jobs import populate_job_data
from app.tasks.scheduler import BackgroundTasks

app = FastAPI()

# Include router
app.include_router(router)

app.mount("/", sio_app)

populate_item_data()

populate_job_data()

BackgroundTasks().run()
