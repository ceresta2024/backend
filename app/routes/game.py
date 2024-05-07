# routes/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import GameController
from app.models.base import get_session
from app.schemas.game import RewardRequest

from app.utils.auth_bearer import JWTBearer
from app.utils.common import get_user_data

router = APIRouter()
namespace = "game"


@router.get("/get_starttime/")
async def get_starttime(session: Session = Depends(get_session)):
    return GameController(session).get_launch_time()


@router.get("/is_opened/")
async def is_opened(session: Session = Depends(get_session)):
    return GameController(session).is_opened()


@router.post("/get_roomlist/")
async def get_roomlist(
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return GameController(session).get_room_list()


@router.post("/add_room/")
async def add_room(
    room_name: str,
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    user_data = get_user_data(token)
    return GameController(session).add_room(room_name, user_data)


@router.post("/add_user/")
async def add_user(
    room_id: str,
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    user_data = get_user_data(token)
    return GameController(session).add_user(room_id, user_data)


@router.post("/get_reward/")
async def get_reward(
    reward: RewardRequest,
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    user_data = get_user_data(token)
    return GameController(session).get_reward(reward, user_data)
