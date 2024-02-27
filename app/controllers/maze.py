from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from fastapi import HTTPException, status

from app.schemas.maze import MapData
from app.utils.gamemap import generate_map
from app.utils.const import MAP_WIDTH, MAP_HEIGHT

from app.schemas.maze import RewardRequest, RewardResponse

from app.models.user import User, TokenTable
from app.models.item import Item
from app.models.inventory import Inventory
from app.models.user_item_log import UserItemLog


class MazeController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_map_data(self) -> list:
        data = generate_map()

        return MapData(width=MAP_WIDTH, height=MAP_HEIGHT, data=data)


    def get_reward(self, reward: RewardRequest) -> RewardResponse:
        # Get user info
        token = (
            self.session.query(TokenTable)
            .filter(TokenTable.access_token == reward.token)
            .first()
        )
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token"
            )
        
        # Get item randomly
        item = self.session.query(Item).filter_by(type=reward.box_type).order_by(func.random()).first()
        if not item:
            raise HTTPException(status_code=401, detail="Not Found items")

        # Add log in useritemlog
        new_log = UserItemLog(
            user_id=token.user_id, item_id=item.id
        )
        self.session.add(new_log)
        self.session.commit()
        self.session.refresh(new_log)

        # Update inventory with new item
        inven = self.session.query(Inventory).filter(Inventory.item_id == item.id).first()
        if inven is None:
            new_inven = Inventory(
                user_id=token.user_id,
                item_id=item.id,
                quantity=1
            )
            self.session.add(new_inven)
            self.session.commit()
            self.session.refresh(new_inven)
        else:
            inven.quantity += 1
            self.session.commit()

        return RewardResponse(
            id=item.id,
            name=item.name,
            price=item.price
        )

