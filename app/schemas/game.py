from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.schemas.game_result import GameResultRead
from app.schemas.game_set import GameSetRead

class GameBase(BaseModel):
    date: datetime
    
class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: int
    result:   GameResultRead = None
    sets:   List[GameSetRead]
    class Config:
        orm_mode = True