from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql import func

from fastapi import HTTPException, status

from app.utils import GAME
from app.utils.const import SCORES_PER_BOX
from app.scripts.import_items import ITEM_LEVEL

from app.schemas.game import RewardRequest, RewardResponse, RoomResponse

from app.models.user import User
from app.models.item import Item
from app.models.inventory import Inventory
from app.models.user_item_log import UserItemLog


class GameController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_launch_time(self) -> str:
        return GAME.launch_time.strftime("%Y-%m-%d %H:%M:%S")

    def is_opened(self) -> dict:
        return {"opened": GAME.is_opened()}

    def add_room(self, room_name, user_data) -> RoomResponse:
        if not GAME.is_opened():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Request"
            )
        room_id, map_id = GAME.add_room(room_name, user_data)
        return RoomResponse(room_id=room_id, map_id=map_id)

    def add_user(self, room_id, user_data) -> RoomResponse:
        if not GAME.is_opened():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Request"
            )
        room_id, map_id = GAME.add_user(room_id, user_data)
        if map_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Request"
            )
        return RoomResponse(room_id=room_id, map_id=map_id)

    def get_reward(self, reward: RewardRequest, user_data) -> RewardResponse:
        user_id = user_data.get("user_id", user_data.get("username"))
        if not GAME.validate_reward(reward, user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found items"
            )
        if not GAME.update_itembox(reward.room_id, reward.box_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient items"
            )
        GAME.rooms[reward.room_id]["winners"].append(user_id)

        # Get item randomly
        item_level = ITEM_LEVEL.get(reward.box_type.capitalize())
        item = (
            self.session.query(Item)
            .options(
                load_only(
                    Item.id,
                    Item.name,
                    Item.price,
                )
            )
            .filter_by(level=item_level)
            .order_by(func.random())
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found items"
            )

        score = SCORES_PER_BOX[item_level]
        is_nickname = user_data.get("username")
        if (
            is_nickname
        ):  # Return reward info without logging in useritemlog and inventory for nicknam user
            return RewardResponse(
                user_score=score, item_id=item.id, name=item.name, price=item.price
            )

        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
            )

        new_score = user.score + score
        user.score = new_score
        self.session.commit()

        # Add log in useritemlog
        new_log = UserItemLog(user_id=user_id, item_id=item.id, score=score)
        self.session.add(new_log)
        self.session.commit()
        self.session.refresh(new_log)

        # Update inventory with new item
        inven = (
            self.session.query(Inventory).filter(Inventory.item_id == item.id).first()
        )
        if inven is None:
            new_inven = Inventory(user_id=user_id, item_id=item.id, quantity=1)
            self.session.add(new_inven)
            self.session.commit()
            self.session.refresh(new_inven)
        else:
            inven.quantity += 1
            self.session.commit()

        return RewardResponse(
            user_score=new_score, item_id=item.id, name=item.name, price=item.price
        )
