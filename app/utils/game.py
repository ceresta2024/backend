from datetime import datetime, timedelta

from app.schemas.game import RewardRequest
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
        return True
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

    def add_room(self, room_name, user_data):
        room_id = "RM_" + id_generator()
        map_id = 0
        user_id = user_data.get("user_id", user_data.get("username"))
        self.rooms[room_id] = {
            "name": room_name,
            "map_id": map_id,
            "users": [user_id],
            "winners": [],
            "itembox": {
                "opened": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        }
        self.room_count += 1
        return room_id, map_id

    def add_user(self, room_id, user_data):
        user_id = user_data.get("user_id", user_data.get("username"))
        if room_id not in self.rooms:
            return room_id, None
        self.rooms[room_id]["users"].append(user_id)
        return room_id, self.rooms[room_id]["map_id"]

    def update_itembox(self, room_id, box_level):
        itembox = self.rooms[room_id]["itembox"]
        if itembox["opened"] >= const.TOTAL_ITEMBOX_COUNT:
            return False
        box_level = box_level.lower()
        if itembox[box_level] < const.ITEMBOX_COUNT[box_level]:
            itembox[box_level] += 1
            itembox["opened"] += 1
            return True
        return False

    def validate_reward(self, reward: RewardRequest, user_id):
        room_id = reward.room_id
        if room_id not in self.rooms:
            return False
        if reward.map_id != self.rooms[room_id]["map_id"]:
            return False
        if user_id not in self.rooms[room_id]["users"]:
            return False
        if user_id in self.rooms[room_id]["winners"]:
            return False
        return True
