from pydantic import BaseModel


class MapData(BaseModel):
    width: int
    height: int
    data: list


class NewRoomRequest(BaseModel):
    room_name: str
    token: str


class RoomResponse(BaseModel):
    room_id: str
    map_id: int


class RewardRequest(BaseModel):
    room_id: int
    map_id: int
    box_type: int


class RewardResponse(BaseModel):
    id: int
    name: str
    price: int
