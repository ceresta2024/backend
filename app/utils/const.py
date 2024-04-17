ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

# Game
GAME_LAUNCH_PERIOD = 2  # Every 2 hours
GAME_COUNTDWON_TIME = 10  # 10 minutes

# item box
ITEM_TYPE_COMMON = 0
ITEM_TYPE_JOB = 1
ITEM_TYPE_JOB_REQUIREMENT = 2
ITEM_TYPE_EVENT = 3

ITEMBOX_LOW = "low"
ITEMBOX_MEDIUM = "medium"
ITEMBOX_HIGH = "high"

ITEMBOX_COUNT = {
    ITEMBOX_HIGH: 1,
    ITEMBOX_MEDIUM: 3,
    ITEMBOX_LOW: 6,
}

TOTAL_ITEMBOX_COUNT = sum(count for count in ITEMBOX_COUNT.values())

# Job
DEFAULT_ALLOW_GOLD = 100
DEFAULT_SPEED = 20

# Score
SCORES_PER_BOX = [3, 6, 10]
