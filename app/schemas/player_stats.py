from pydantic import BaseModel

class PlayerStats(BaseModel):
    total_games: int
    wins: int
    losses: int
    win_rate: float
    wins_team1: int
    wins_team2: int
    avg_score_for: float
    avg_score_against: float
    avg_score_for_win: float
    
    model_config = {
        "from_attributes": True,
    }
    