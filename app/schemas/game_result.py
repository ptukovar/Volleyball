from typing import Optional
from pydantic import BaseModel

class GameResultBase(BaseModel):
    sets_team1: int
    sets_team2: int
    mvp:        Optional[int] = None
    impostor:   Optional[int] = None

class GameResultCreate(GameResultBase):
    pass

class GameResultRead(GameResultBase):
    id:      int
    game_id: int
    mvp:        Optional[int] = None
    impostor:   Optional[int] = None

    class Config:
        orm_mode = True
