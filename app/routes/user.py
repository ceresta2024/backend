# routes/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from functools import wraps

from app.controllers import UserController
from app.models.base import get_session
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    TokenSchema,
    LoginUserInfo,
    UserInfo,
    RequestDetails,
    ChangePassword,
    SetJob,
    GetReward,
)
from app.utils.auth_bearer import JWTBearer, decodeJWT

router = APIRouter()
namespace = "user"

from fastapi_sso.sso.google import GoogleSSO

CLIENT_ID = "88063403687-6nn4713fc3bb9jpgc9ckj6umhkkfeao1.apps.googleusercontent.com"
CLIENT_SECRET = "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"


def get_google_sso() -> GoogleSSO:
    return GoogleSSO(
        CLIENT_ID,
        CLIENT_SECRET,
        redirect_uri="http://localhost:8000/user/google_callback",
    )


@router.get("/google_login")
async def google_login(google_sso: GoogleSSO = Depends(get_google_sso)):
    return await google_sso.get_login_redirect()


@router.get("/google_callback")
async def google_callback(
    request: RequestDetails, google_sso: GoogleSSO = Depends(get_google_sso)
):
    user = await google_sso.verify_and_process(request)
    return user


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs["dependencies"]
        session = kwargs["session"]

        user_id = decodeJWT(token)["sub"]
        data = UserController(session).token_required(token, user_id)
        if data:
            return func(token, session)
        else:
            return {"msg": "Token blocked"}

    return wrapper


@router.post("/register/")
async def register(user: UserCreate, session: Session = Depends(get_session)):
    return UserController(session).register(user)


@router.post("/login/", response_model=LoginUserInfo)
async def login(request: RequestDetails, session: Session = Depends(get_session)):
    return UserController(session).login(request)


@router.post("/logout")
def logout(token=Depends(JWTBearer()), session: Session = Depends(get_session)):
    user_id = decodeJWT(token)["sub"]
    return UserController(session).logout(token, user_id)


@router.post("/getinfo", response_model=UserInfo)
def get_user_info(token=Depends(JWTBearer()), session: Session = Depends(get_session)):
    user_id = decodeJWT(token)["sub"]
    return UserController(session).get_info(user_id)


@router.get("/getusers")
def getusers(token=Depends(JWTBearer()), session: Session = Depends(get_session)):
    return UserController(session).get_users()


@router.post("/change_account/")
async def change_account(session: Session = Depends(get_session)):
    return UserController(session).change_password()


@router.post("/change_password/")
async def change_password(
    request: ChangePassword,
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return UserController(session).change_password(request)


@router.get("/get_nickname/")
async def get_nickname(session: Session = Depends(get_session)):
    return UserController(session).get_nickname()


@router.get("/get_gold/")
async def get_gold(token=Depends(JWTBearer()), session: Session = Depends(get_session)):
    user_id = decodeJWT(token)["sub"]
    return UserController(session).get_money(user_id)


@router.get("/get_score/")
async def get_score(
    token=Depends(JWTBearer()), session: Session = Depends(get_session)
):
    user_id = decodeJWT(token)["sub"]
    return UserController(session).get_score(user_id)


### Job apis
@router.get("/get_jobs/")
async def get_jobs(token=Depends(JWTBearer()), session: Session = Depends(get_session)):
    return UserController(session).get_jobs()


@router.post("/set_job/")
async def set_job(
    request: SetJob,
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    user_id = decodeJWT(token)["sub"]
    return UserController(session).set_job(request, user_id)


@router.get("/get_notice/")
async def get_notice(session: Session = Depends(get_session)):
    return UserController(session).get_notice()


@router.post("/get_reward/")
async def get_reward(
    request: GetReward,
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    user_id = decodeJWT(token)["sub"]
    return UserController(session).get_reward(request, user_id)
