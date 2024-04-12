from datetime import datetime, timedelta

from app.utils import const


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rooms = {}
        self.room_count = 0
        self.launch_time = self.get_launch_time()

    def get_launch_time(self):
        now = datetime.utcnow()
        next_hour = (
            now.hour // const.GAME_LAUNCH_PERIOD + 1
        ) * const.GAME_LAUNCH_PERIOD
        diff_hour = next_hour - now.hour
        normal_now = now.replace(minute=0, second=0, microsecond=0)
        return normal_now + timedelta(hours=diff_hour)

    def initalize(self):
        now = datetime.utcnow()
        if now < self.launch_time + timedelta(minutes=const.GAME_COUNTDWON_TIME):
            return
        self.reset()

    def add_room(self, room_name):
        self.rooms[room_name] = {
            "user": [],
            "itembox": {
                "opened": 0,
                "level": {"high": 0, "medium": 0, "low": 0},
            },
        }
        self.room_count += 1

    def add_user(self, room_name, user_id):
        self.rooms[room_name]["users"].append(user_id)
