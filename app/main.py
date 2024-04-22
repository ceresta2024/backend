# main.py

from fastapi import FastAPI
from app.config import settings
from app.routes import router
from app.sockets import sio_app
from app.scripts import populate_db
from app.tasks.scheduler import BackgroundTasks
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

parent_directory = Path(__file__).parent
static_path = parent_directory / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Include router
app.include_router(router)

app.mount("/", sio_app)

populate_db()

BackgroundTasks().run()
