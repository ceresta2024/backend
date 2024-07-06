# routes/user.py
from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from sqlalchemy.orm import Session
from functools import wraps

from app.controllers import UserController
from app.models.base import get_session

from app.schemas.user import (
    UserCreate,
    LoginUserInfo,
    UserInfo,
    RequestDetails,
    ChangePassword,
    SetJob,
)
from app.utils.auth_bearer import JWTBearer, decodeJWT
from app.utils.const import (
    HOST_URL,
    SESSION_COOKIE_NAME,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    FACEBOOK_CLIENT_ID,
    FACEBOOK_CLIENT_SECRET,
)

from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO

router = APIRouter()
namespace = "user"

google_sso = GoogleSSO(
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, f"{HOST_URL}/user/google_callback"
)


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


@router.get("/google_login", tags=["Google SSO"])
async def google_login():
    with google_sso:
        return await google_sso.get_login_redirect(
            params={"prompt": "consent", "access_type": "offline"}
        )


@router.get("/google_callback", tags=["Google SSO"])
async def google_callback(request: Request, session: Session = Depends(get_session)):
    with google_sso:
        user = await google_sso.verify_and_process(request)
    user_info = UserCreate(
        username=user.display_name,
        email=user.email,
        password=user.provider + user.first_name,
    )
    access_token = UserController(session).callback_sso(user_info, user.provider)
    response = RedirectResponse(url="/admin/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(SESSION_COOKIE_NAME, access_token)
    return response


facebook_sso = FacebookSSO(
    FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, f"{HOST_URL}/user/facebook_callback"
)


@router.get("/facebook_login", tags=["Facebook SSO"])
async def facebook_login():
    with facebook_sso:
        return await facebook_sso.get_login_redirect()


@router.get("/facebook_callback", tags=["Facebook SSO"])
async def facebook_callback(request: Request, session: Session = Depends(get_session)):
    """Process login response from Facebook and return user info"""
    with facebook_sso:
        user = await facebook_sso.verify_and_process(request)
    user_info = UserCreate(
        username=user.display_name,
        email=user.email,
        password=user.provider + user.first_name,
    )
    access_token = UserController(session).callback_sso(user_info, user.provider)
    response = RedirectResponse(url="/admin/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(SESSION_COOKIE_NAME, access_token)
    return response


@router.post("/register/")
async def register(user: UserCreate, session: Session = Depends(get_session)):
    return UserController(session).register(user)


@router.post("/login/", response_model=LoginUserInfo)
async def login(request: RequestDetails, session: Session = Depends(get_session)):
    return UserController(session).login(request)


@router.post("/logout")
def logout(token=Depends(JWTBearer()), session: Session = Depends(get_session)):
    user_id = decodeJWT(token)["sub"]
    UserController(session).logout(token, user_id)
    response = RedirectResponse(url="/admin/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


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


@router.get("/get_rankings")
async def get_rankings(
    token=Depends(JWTBearer()), session: Session = Depends(get_session)
):
    return UserController(session).get_rankings()


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
