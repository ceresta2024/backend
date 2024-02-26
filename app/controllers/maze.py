from sqlalchemy.orm import Session

from app.schemas.maze import MapData
from app.utils.gamemap import generate_map
from app.utils.const import MAP_WIDTH, MAP_HEIGHT


class MazeController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_map_data(self) -> list:
        data = generate_map()

        return MapData(width=MAP_WIDTH, height=MAP_HEIGHT, data=data)
