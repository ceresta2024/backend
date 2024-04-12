from datetime import datetime, timedelta

from app.utils import const
from app.utils.common import id_generator

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rooms = {}
        self.room_count = 0
        self.launch_time = self.get_launch_time()
        self.down_time = self.launch_time + timedelta(minutes=const.GAME_COUNTDWON_TIME)

    def is_opened(self):
        now = datetime.utcnow()
        if self.launch_time <= now and now < self.down_time:
            return True
        return False

    def get_launch_time(self):
        now = datetime.utcnow()
        next_hour = (
            now.hour // const.GAME_LAUNCH_PERIOD + 1
        ) * const.GAME_LAUNCH_PERIOD
        diff_hour = next_hour - now.hour
        normal_now = now.replace(minute=0, second=0, microsecond=0)
        return normal_now + timedelta(hours=diff_hour)

    def add_room(self, room_name, user_id):
        room_id = id_generator()
        map_id = 0
        self.rooms[room_id] = {
            "name": room_name,
            "map_id": map_id,
            "users": [user_id],
            "itembox": {
                "opened": 0,
                "level": {"high": 0, "medium": 0, "low": 0},
            },
        }
        self.room_count += 1
        return room_id, map_id

    def add_user(self, room_name, user_id):
        self.rooms[room_name]["users"].append(user_id)
