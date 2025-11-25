from pydantic import BaseModel

class GameSetBase(BaseModel):
    set_number:  int
    team1_score: int
    team2_score: int

class GameSetCreate(GameSetBase):
    pass

class GameSetRead(GameSetBase):
    id:      int
    game_id: int

    class Config:
        orm_mode = True
