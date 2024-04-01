# routes/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from functools import wraps

from app.controllers import UserController
from app.models.base import get_session
from app.models.user import User

from app.schemas.user import UserCreate, TokenSchema, RequestDetails, ChangePassword
from app.utils.auth_bearer import JWTBearer, decodeJWT

router = APIRouter()
namespace = "user"


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs["dependencies"]
        session = kwargs["session"]

        payload = decodeJWT(token)
        user_id = payload["sub"]
        data = UserController(session).token_required(token, user_id)
        if data:
            return func(token, session)
        else:
            return {"msg": "Token blocked"}

    return wrapper


@router.post("/register/")
async def register(user: UserCreate, session: Session = Depends(get_session)):
    return UserController(session).register(user)


@router.post("/login/", response_model=TokenSchema)
async def login(request: RequestDetails, session: Session = Depends(get_session)):
    return UserController(session).login(request)


@router.post("/logout")
def logout(dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    token = dependencies
    payload = decodeJWT(token)
    user_id = payload["sub"]

    return UserController(Session).logout(token, user_id)


@router.get("/getusers")
def getusers(
    dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)
):
    return UserController(session).get_users()


@router.post("/change_account/")
async def change_account(session: Session = Depends(get_session)):
    return UserController(session).change_password()


@router.post("/change_password/")
async def change_password(
    request: ChangePassword,
    dependencies=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return UserController(session).change_password(request)


@router.get("/get_nickname/")
async def get_nickname(session: Session = Depends(get_session)):
    return UserController(session).get_nickname()


@router.get("/get_gold/")
async def get_nickname(
    dependencies=Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    token = dependencies
    payload = decodeJWT(token)
    user_id = payload["sub"]

    return UserController(session).get_money(user_id)

