# routes/admin.py
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import APIKeyCookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from importlib.metadata import version
from pathlib import Path

from app.models.base import get_session

from app.utils.const import (
    SESSION_COOKIE_NAME,
)

router = APIRouter()
namespace = "admin"

parent_directory = Path(__file__).parent
templates_path = parent_directory.parent / "templates"
templates = Jinja2Templates(directory=templates_path)

COOKIE = APIKeyCookie(name=SESSION_COOKIE_NAME, auto_error=False)


@router.get("/", response_class=HTMLResponse, summary="Home page")
def home_page(
    request: Request,
    session: Session = Depends(get_session),
    session_token: str = Depends(COOKIE),
):
    """
    Returns all users.
    """
    versions = {
        "fastapi_version": version("fastapi"),
        "fastapi_sso_version": version("fastapi_sso"),
    }
    try:
        if session_token:
            user = {"username": "TESTUSER", "provider": "GOOGLE"}
            response = templates.TemplateResponse(
                "index.html", {"request": request, "user": user, **versions}
            )
        else:
            response = templates.TemplateResponse(
                "login.html", {"request": request, **versions}
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )
