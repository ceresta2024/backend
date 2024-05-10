import schedule
import time

from datetime import datetime
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

    def initalize_game_data(self):
        if datetime.utcnow() > GAME.down_time:
            GAME.reset()

    def reset_weather(self):
        GAME.set_weather()

    def init_schedule_jobs(self):
        schedule.every(1).minutes.do(self.initalize_game_data)
        schedule.every(10).minutes.do(self.reset_weather)  # for testing.

    def run_schedule_jobs(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        T = Thread(target=self.run_schedule_jobs)
        T.setDaemon(True)
        T.start()
