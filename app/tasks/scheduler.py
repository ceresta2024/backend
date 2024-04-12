import schedule
import time

from threading import Thread

from app.tasks import celery
from app.utils import GAME


@celery.task(name="app.tasks.create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


class BackgroundTasks:
    def __init__(self) -> None:
        self.init_schedule_jobs()

    def check_live(self):
        print("Server is live")

    def update_room_data(self):
        GAME.update_data()

    def init_schedule_jobs(self):
        schedule.every(1).minutes.do(self.check_live)
        schedule.every(10).seconds.do(self.update_room_data)

    def run_schedule_jobs(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        T = Thread(target=self.run_schedule_jobs)
        T.setDaemon(True)
        T.start()
