# main.py

from fastapi import FastAPI
from app.config import settings
from app.routes import router
from app.sockets import sio_app
from app.scripts import populate_db
from app.tasks.scheduler import BackgroundTasks

app = FastAPI()

# Include router
app.include_router(router)

app.mount("/", sio_app)

populate_db()

BackgroundTasks().run()
