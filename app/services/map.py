from datetime import datetime

from app.main import celery


def generate_map():
    return [100, 100]


@celery.task(name="app.celery.worker.get_maze_opening_time")
def get_maze_opening_time():
    return datetime.utcnow()
