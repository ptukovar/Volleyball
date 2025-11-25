from pydantic import BaseModel

class GamePlayerBase(BaseModel):
    player_id: int
    team: int
    
class GamePlayerCreate(GamePlayerBase):
    pass

class GamePlayerRead(GamePlayerBase):
    id: int
    game_id: int
    
    class Config:
        orm_mode = True
