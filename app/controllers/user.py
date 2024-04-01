from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User, TokenTable
from app.schemas.user import UserCreate, RequestDetails, NickToken, ChangePassword

from app.utils.common import (
    id_generator,
    create_access_token,
    verify_password,
    create_refresh_token,
    get_hashed_password,
)


class UserController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def token_required(self, token: str, user_id: int):
        return (
            self.session.query(TokenTable)
            .filter_by(user_id=user_id, access_toke=token, status=True)
            .first()
        )

    def register(self, user: UserCreate):
        existing_user = (
            self.session.query(User).filter_by(user_name=user.username).first()
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="User name already registered")
        existing_user = self.session.query(User).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        encrypted_password = get_hashed_password(user.password)

        new_user = User(
            user_name=user.username, email=user.email, password=encrypted_password
        )

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return {"message": "user created successfully"}

    def login(self, request: RequestDetails):
        user = self.session.query(User).filter(User.email == request.email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email"
            )
        hashed_pass = user.password
        if not verify_password(request.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )

        access = create_access_token(user.id)
        refresh = create_refresh_token(user.id)

        token_db = TokenTable(
            user_id=user.id, access_token=access, refresh_token=refresh, status=True
        )
        self.session.add(token_db)
        self.session.commit()
        self.session.refresh(token_db)
        return {
            "access_token": access,
            "refresh_token": refresh,
        }

    def logout(self, token: str, user_id: int):
        token_record = self.session.query(TokenTable).all()
        info = []
        for record in token_record:
            print("record", record)
            if (datetime.utcnow() - record.created_date).days > 1:
                info.append(record.user_id)
        if info:
            existing_token = (
                self.session.query(TokenTable)
                .where(TokenTable.user_id.in_(info))
                .delete()
            )
            self.session.commit()

        existing_token = (
            self.session.query(TokenTable)
            .filter(TokenTable.user_id == user_id, TokenTable.access_token == token)
            .first()
        )
        if existing_token:
            existing_token.status = False
            self.session.add(existing_token)
            self.session.commit()
            self.session.refresh(existing_token)

        return {"message": "Logout Successfully"}

    def change_password(self, request: ChangePassword):
        if request.old_password == request.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not allowed same new password",
            )

        user = self.session.query(User).filter(User.email == request.email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
            )

        if not verify_password(request.old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password"
            )

        encrypted_password = get_hashed_password(request.new_password)
        user.password = encrypted_password
        self.session.commit()

        return {"message": "Password changed successfully"}

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

    def get_nickname(self) -> NickToken:
        now = datetime.utcnow()
        str_time = now.strftime("%m%d%y%H%M%S")
        uid = id_generator()
        nickname = f"{uid}_{str_time}"
        token = create_access_token({"username": nickname})

        return NickToken(username=nickname, access_token=token)

    def get_users(self) -> list[User]:
        return self.session.query(User).all()

    def get_money(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect token"
            )
        game_money = 0 if user.game_money is None else user.game_money
        return {
            "gold": game_money,
        }
