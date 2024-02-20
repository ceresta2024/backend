import time

from datetime import datetime

from app.tasks import celery


@celery.task(name="app.tasks.get_maze_opening_time")
def get_maze_opening_time():
    return datetime.utcnow()


@celery.task(name="app.tasks.create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
