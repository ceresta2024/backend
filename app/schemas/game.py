from pydantic import BaseModel


class MapData(BaseModel):
    width: int
    height: int
    data: list


class RewardRequest(BaseModel):
    map_id: int
    box_type: int
    token: str


class RewardResponse(BaseModel):
    id: int
    name: str
    price: int
