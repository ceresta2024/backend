from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, load_only

from app.models.user import User, TokenTable, Job
from app.models.inventory import Inventory
from app.models.item import Item
from app.models.notice import Notice
from app.schemas.user import (
    UserCreate,
    RequestDetails,
    NickToken,
    ChangePassword,
    SetJob,
    ItemList,
    JobList,
    RankingList,
)
from app.utils import JOBS
from app.utils.common import (
    id_generator,
    create_access_token,
    verify_password,
    create_refresh_token,
    get_hashed_password,
    get_list_of_dict,
)
from app.utils.const import (
    ITEM_TYPE_JOB_REQUIREMENT,
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

    def callback_sso(self, user: UserCreate, provider: str):
        existing_user = (
            self.session.query(User).filter_by(user_name=user.username).first()
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="User name already registered")
        existing_user = self.session.query(User).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create new user from google
        encrypted_password = get_hashed_password(user.password)
        new_user = User(
            user_name=user.username, email=user.email, password=encrypted_password
        )
        self.session.add(new_user)
        self.session.flush()
        self.session.commit()
        self.session.refresh(new_user)

        # Create access token
        access_token = create_access_token(new_user.id)
        refresh_token = create_refresh_token(new_user.id)
        token_db = TokenTable(
            user_id=new_user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            status=True,
        )
        self.session.add(token_db)
        self.session.commit()
        self.session.refresh(token_db)

        return access_token

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

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        token_db = TokenTable(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            status=True,
        )
        self.session.add(token_db)
        self.session.commit()
        self.session.refresh(token_db)

        return {**user.info, "access_token": access_token}

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
        uid = id_generator()
        nickname = f"{uid}{now.microsecond}"[:-3]
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

    def get_rankings(self):
        rows = (
            self.session.query(User.user_name, User.job_id, User.score)
            .order_by(User.score.desc())
            .limit(50)
        )
        rankings = get_list_of_dict(RankingList.__fields__.keys(), rows)
        for ranking in rankings:
            ranking["job"] = JOBS["ID_TO_NAME"].get(ranking["job"], "")
        return {"data": rankings}

    def get_jobs(self):
        rows = (
            self.session.query(
                Job.id, Job.name, Job.description, Job.speed, Job.allow_gold
            )
            .filter(Job.id > 0, Job.enabled == True)
            .all()
        )
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
            ).filter(Item.type == ITEM_TYPE_JOB_REQUIREMENT, Item.job_id == job["id"])
            items = get_list_of_dict(ItemList.__fields__.keys(), records)
            job["items"] = items
        return {"data": jobs}

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

        # Check if user is already set as this job
        if user.job_id == job.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User already set as {job.name}",
            )

        # Check if user is eligible for setting job
        if user.game_money < job.allow_gold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User's game money insufficient",
            )
        items = self.session.query(Item.id, Item.name).filter(
            Item.type == ITEM_TYPE_JOB_REQUIREMENT, Item.job_id == job.id
        )
        item_list = dict((item.id, item.name) for item in items)
        inven = self.session.query(Inventory).filter(
            Inventory.user_id == user.id,
            Inventory.item_id.in_(item_list),
            Inventory.quantity > 0,
        )
        inven_item_list = dict((inv.item_id, inv.quantity) for inv in inven)
        diff_item_ids = list(set(item_list.keys()) - set(inven_item_list.keys()))
        if len(diff_item_ids) > 0:
            diff_item_names = [v for k, v in item_list.items() if k in diff_item_ids]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User inventory item insufficient: {', '.join(diff_item_names)}",
            )

        # Set user job and update user game_money and inventory item
        user.game_money -= job.allow_gold
        user.job_id = request.job_id
        for inv in inven:
            inv.quantity -= 1

        self.session.commit()

        return {"message": "Set job successfully"}

    def get_notice(self):
        return (
            self.session.query(Notice)
            .options(
                load_only(
                    Notice.name, Notice.contents, Notice.start_date, Notice.end_date
                )
            )
            .filter(Notice.is_available == 1)
            .all()
        )
