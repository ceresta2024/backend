from sqlalchemy.orm import Session

from app.utils.gamemap import generate_map


class MazeController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_map_data(self) -> list:
        data = generate_map()

        return data
