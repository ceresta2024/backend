from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from fastapi import HTTPException, status

from app.utils import GAME

from app.utils.auth_bearer import decodeJWT

from app.schemas.game import RewardRequest, RewardResponse, RoomResponse

from app.models.user import User, TokenTable
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
        if GAME.validate_reward(reward, user_data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found items"
            )
        if not GAME.update_itembox(reward.room_id, reward.box_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient items"
            )

        is_nickname = user_data.get("username")

        # Get item randomly
        item = (
            self.session.query(Item)
            .filter_by(type=reward.box_type)
            .order_by(func.random())
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found items"
            )

        if (
            is_nickname
        ):  # Return reward info without logging in useritemlog and inventory for nicknam user
            return RewardResponse(id=item.id, name=item.name, price=item.price)

        user_id = user_data["user_id"]

        # Add log in useritemlog
        new_log = UserItemLog(user_id=user_id, item_id=item.id)
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

        return RewardResponse(id=item.id, name=item.name, price=item.price)
