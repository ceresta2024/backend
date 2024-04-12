# routes/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import GameController
from app.models.base import get_session
from app.schemas.game import RewardRequest

from app.utils.auth_bearer import JWTBearer

router = APIRouter()
namespace = "game"


@router.get("/get_starttime/")
async def get_starttime(session: Session = Depends(get_session)):
    return GameController(session).get_launch_time()


@router.get("/is_opened/")
async def is_opened(session: Session = Depends(get_session)):
    return GameController(session).is_opened()


@router.post("/get_reward/")
async def get_reward(
    reward: RewardRequest,
    session: Session = Depends(get_session),
):
    return GameController(session).get_reward(reward)
