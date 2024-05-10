from datetime import datetime, timedelta
from random import choice

from app.config import settings
from app.schemas.game import RewardRequest
from app.utils import const
from app.utils.common import id_generator

INITIAL_ROOM_COUNT = 12


class Game:
    def __init__(self):
        self.reset()
        self.set_weather()

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
        if settings.ENV == "dev":
            min = (now.minute // 10) * 10
            normal_now = now.replace(minute=min, second=0, microsecond=0)
            return normal_now + timedelta(minutes=10)
        else:
            next_hour = (
                now.hour // const.GAME_LAUNCH_PERIOD + 1
            ) * const.GAME_LAUNCH_PERIOD
            diff_hour = next_hour - now.hour
            normal_now = now.replace(minute=0, second=0, microsecond=0)
            return normal_now + timedelta(hours=diff_hour)

    def set_weather(self):
        self.weather = choice(const.WEATHER)

    def get_room_list(self):
        if len(self.rooms) < INITIAL_ROOM_COUNT:
            self.set_weather()
            for _ in range(INITIAL_ROOM_COUNT):
                room_id = "RM_" + id_generator()
                map_id = 3
                self.rooms[room_id] = {
                    "map_id": map_id,
                    "users": [],
                    "winners": [],
                    "itembox": {
                        "opened": 0,
                        "high": 0,
                        "medium": 0,
                        "low": 0,
                    },
                }
            self.room_count = INITIAL_ROOM_COUNT
        rooms = [
            {"room_id": room_id, "map_id": room["map_id"], "weather": self.weather}
            for room_id, room in self.rooms.items()
        ]
        return rooms

    def add_room(self, room_name, user_data):
        room_id = "RM_" + id_generator()
        map_id = 3
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

    def remove_user(self, room_id, user_data):
        user_id = user_data.get("user_id", user_data.get("username"))
        if room_id not in self.rooms:
            return False
        if user_id in self.rooms[room_id]["users"]:
            self.rooms[room_id]["users"].remove(user_id)
            return True
        return False

    def get_box_type(self, room_id):
        opened_boxes = self.rooms[room_id]["itembox"]["opened"]
        if opened_boxes >= const.TOTAL_ITEMBOX_COUNT:
            return None

        for box_type, box_count in const.ITEMBOX_COUNT.items():
            if opened_boxes < box_count:
                self.rooms[room_id]["itembox"]["opened"] += 1
                return box_type
            opened_boxes -= box_count

        return None

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
