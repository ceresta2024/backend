from app.utils import const
from app.utils.map.map_generator import get_gmap_array
from app.utils.map.map_entities import GameMapSettings

from datetime import datetime, timedelta


def get_game_launch_time():
    now = datetime.utcnow()
    next_hour = (now.hour // const.GAME_LAUNCH_PERIOD + 1) * const.GAME_LAUNCH_PERIOD
    diff_hour = next_hour - now.hour
    normal_now = now.replace(minute=0, second=0, microsecond=0)
    launch_time = normal_now + timedelta(hours=diff_hour)
    return launch_time.strftime("%Y-%m-%d %H:%M:%S")


def init_map_settings(map_settings):
    map_width = const.MAP_WIDTH
    map_height = const.MAP_HEIGHT
    map_settings.size = (map_height, map_width)
    map_settings.block_settings.seeds_amount = const.MAP_BLOCK_SEEDS_AMOUNT
    map_settings.block_settings.growth_rate = const.MAP_BLOCK_GROWTH_RATE
    map_settings.wall_settings.wall_seeds_count = const.MAP_WALL_SEEDS_AMOUNT
    map_settings.wall_settings.wall_length = const.MAP_WALL_GROWTH_RATE
    map_settings.grass_settings.seeds_amount = const.MAP_GRASS_SEEDS_AMOUNT
    map_settings.grass_settings.growth_rate = const.MAP_GRASS_GROWTH_RATE
    map_settings.tunnel_settings.seeds_amount = const.MAP_TUNNEL_SEEDS_AMOUNT
    map_settings.tunnel_settings.growth_rate = const.MAP_TUNNEL_GROWTH_RATE
    map_settings.pit_settings.seeds_amount = const.MAP_PIT_SEEDS_AMOUNT
    map_settings.pit_settings.growth_rate = const.MAP_PIT_GROWTH_RATE
    map_settings.thorn_settings.seeds_amount = const.MAP_THORN_SEEDS_AMOUNT
    map_settings.thorn_settings.growth_rate = const.MAP_THORN_GROWTH_RATE

    map_settings.pos_type = {
        "block": const.MAPPOS_TYPE_BLOCK,
        "field": const.MAPPOS_TYPE_BLOCK,
        "wall": const.MAPPOS_TYPE_WALL,
        "grass": const.MAPPOS_TYPE_GRASS,
        "tunnel": const.MAPPOS_TYPE_TUNNEL,
        "pit": const.MAPPOS_TYPE_PIT,
        "thorn": const.MAPPOS_TYPE_THORN,
    }


def generate_map():
    map_settings = GameMapSettings()
    init_map_settings(map_settings)
    data = get_gmap_array(map_settings)
    return data
