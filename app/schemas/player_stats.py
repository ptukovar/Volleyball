from pydantic import BaseModel

class PlayerStats(BaseModel):
    total_games: int
    wins: int
    losses: int
    win_rate: float
    wins_team1: int
    wins_team2: int
    total_sets: int
    sets_won: int
    sets_lost: int
    sets_win_rate: float
    avg_winning_points: float
    avg_losing_points: float
    avg_points: float
    mvp_count: int
    impostor_count: int
    
    class Config:
        orm_mode = True
    