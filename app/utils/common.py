import random
import string

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from app.config import settings
from app.utils.const import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta

    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def get_list_of_dict(keys, list_of_tuples):
    """
    This function will accept keys and list_of_tuples as args and return list of dicts
    """
    list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
    return list_of_dict
