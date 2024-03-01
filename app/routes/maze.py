# routes/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import MazeController
from app.models.base import get_session
from app.schemas.maze import RewardRequest

from app.utils.auth_bearer import JWTBearer

router = APIRouter()
namespace = "maze"


@router.get("/get_starttime/")
async def get_starttime(session: Session = Depends(get_session)):
    return MazeController(session).get_launch_time()


@router.get("/is_open/")
async def is_open():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/get_map_data/")
async def get_map_data(session: Session = Depends(get_session)):
    return MazeController(session).get_map_data()


@router.post("/get_reward/")
async def get_reward(
    reward: RewardRequest,
    # dependencies=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return MazeController(session).get_reward(reward)
