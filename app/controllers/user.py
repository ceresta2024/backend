from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql.expression import func

from app.models.user import User, TokenTable, Job
from app.models.item import Item
from app.models.user_item_log import UserItemLog
from app.models.notice import Notice
from app.schemas.user import (
    UserCreate,
    RequestDetails,
    NickToken,
    ChangePassword,
    SetJob,
    GetReward,
    ItemList,
    JobList,
)
from app.utils.common import (
    id_generator,
    create_access_token,
    verify_password,
    create_refresh_token,
    get_hashed_password,
    get_list_of_dict,
)
from app.utils.const import SCORES_PER_BOX


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

        return {**user.info, "access_token": access}

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

    def get_info(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect token"
            )

        return user.info

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

    def get_score(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect token"
            )
        return {
            "score": user.score,
        }

    def get_jobs(self):
        rows = self.session.query(
            Job.id, Job.name, Job.description, Job.speed, Job.allow_gold
        ).all()
        jobs = get_list_of_dict(JobList.__fields__.keys(), rows)
        for job in jobs:
            records = self.session.query(
                Item.id,
                Item.name,
                Item.description,
                Item.price,
                Item.hp,
                Item.sp,
                Item.img_path,
            ).filter(Item.type == 2, Item.job_id == job["id"])
            items = get_list_of_dict(ItemList.__fields__.keys(), records)
            job["items"] = items
        return jobs

    def set_job(self, request: SetJob, user_id: int):
        job = self.session.query(Job).filter(Job.id == request.job_id).first()
        if job is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Job not found"
            )

        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
            )

        user.job_id = request.job_id
        self.session.commit()

        return {"message": "Set job successfully"}

    def get_notice(self):
        return (
            self.session.query(Notice)
            .options(load_only(Notice.contents, Notice.type))
            .filter(Notice.is_available == 1)
            .all()
        )

    def get_reward(self, request: GetReward, user_id: int):
        ### Adds score by box into user's score
        score = SCORES_PER_BOX[request.box_id]
        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
            )

        new_score = user.score + score
        user.score = new_score
        self.session.commit()

        ### Choose item in random from items table
        item = (
            self.session.query(Item)
            .options(
                load_only(
                    Item.id,
                    Item.name,
                    Item.description,
                    Item.img_path,
                    Item.price,
                    Item.type,
                )
            )
            .filter(Item.level == request.box_id)
            .order_by(func.random())
            .first()
        )
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not chosen"
            )

        ### Save the log for reward
        new_item_log = UserItemLog(user_id=user_id, item_id=item.id, score=score)
        self.session.add(new_item_log)
        self.session.commit()

        return {
            "user_score": new_score,
            "item_id": item.id,
            "item_name": item.name,
            "item_desc": item.description,
            "item_img": item.img_path,
            "item_price": item.price,
        }
