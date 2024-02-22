from datetime import datetime

from sqlalchemy.orm import Session
from app.models.user import User
import app.schemas.user as schema

from app.utils.common import id_generator, create_access_token


class UserController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def verify_email(self, email: str) -> bool:
        if self.session.query(User).filter_by(email=email).first():
            return True
        return False

    def verify_username(self, username: str) -> bool:
        if self.session.query(User).filter_by(username=username).first():
            return True
        return False

    def get_user_detail(self, username: str) -> User:
        return self.session.query(User).filter_by(username=username).first()

    def get_nickname(self) -> schema.NickToken:
        now = datetime.utcnow()
        str_time = now.strftime("%m%d%y%H%M%S")
        uid = id_generator()
        nickname = f"{uid}_{str_time}"
        token = create_access_token({"username": nickname})

        return schema.NickToken(username=nickname, access_token=token)
