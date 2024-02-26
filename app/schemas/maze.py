from pydantic import BaseModel


class MapData(BaseModel):
    width: int
    height: int
    data: list
