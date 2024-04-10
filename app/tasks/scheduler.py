import schedule
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


class BackgroundTasks:
    def __init__(self) -> None:
        self.init_schedule_jobs()

    def check_live(self):
        print("Server is live")

    def init_schedule_jobs(self):
        schedule.every(1).minutes.do(self.check_live)

    def run_schedule_jobs(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
