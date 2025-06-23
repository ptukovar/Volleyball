from pydantic import BaseModel

class GameResultBase(BaseModel):
    team1_score: int
    team2_score: int

class GameResultCreate(GameResultBase):
    id: int
    game_id: int
    
class GameResultRead(GameResultBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }
        