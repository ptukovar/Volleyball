from pydantic import BaseModel

class GamePlayerBase(BaseModel):
    player_id: int
    team: int
    
class GamePlayerCreate(GamePlayerBase):
    pass

class GamePlayerRead(GamePlayerBase):
    id: int
    game_id: int
    
    model_config = {
        "from_attributes": True
    }
