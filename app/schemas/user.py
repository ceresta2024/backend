from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=5)
    email: EmailStr
    password: str = Field(min_length=8)

    @validator("password")
    @classmethod
    def validate_password(cls, value):
        min_length = 8
        errors = ""
        if len(value) < min_length:
            errors += "Password must be at least 8 characters long. "
        if not any(character.islower() for character in value):
            errors += "Password should contain at least one lowercase character."
        if errors:
            raise ValueError(errors)

        return value


class RequestDetails(BaseModel):
    email: str = Field(min_length=5)
    password: str = Field(min_length=5)


class NickToken(BaseModel):
    username: str = Field(min_length=5)
    access_token: str = Field(min_length=10)


class TokenSchema(BaseModel):
    access_token: str = Field(min_length=10)
    refresh_token: str = Field(min_length=10)


class UserInfo(BaseModel):
    id: int
    name: str = Field(min_length=5)
    email: str = Field(min_length=5)
    gold: int
    score: int
    job: str = Field(nullable=True)
    status: Optional[int] = Field(nullable=True)


class LoginUserInfo(UserInfo):
    access_token: str = Field(min_length=10)


class ChangePassword(BaseModel):
    email: EmailStr
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)


class SetJob(BaseModel):
    job_id: int


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime


class ItemList(BaseModel):
    id: int
    name: str
    description: str
    price: int
    hp: int
    sp: int
    img_path: str


class JobList(BaseModel):
    id: int
    name: str
    description: str
    speed: int
    allow_gold: int
    items: list[ItemList]


class RankingList(BaseModel):
    name: str
    job: int
    score: int
