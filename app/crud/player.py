from sqlalchemy.orm import Session
from app.models.player import Player
from app.models.game_player import GamePlayer
from app.models.game_result import GameResult
from app.schemas.player import PlayerCreate
from app.schemas.player_stats import PlayerStats

def create_player(db: Session, player: PlayerCreate) -> Player:
    db_player = Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_player(db: Session, player_id: int) -> Player:
    return db.query(Player).filter(Player.id == player_id).first()

def get_player_stats(db: Session, player_id: int) -> PlayerStats:
    player = get_player(db, player_id)
    results = (
        db.query(GamePlayer, GameResult)
        .join(GameResult, GamePlayer.game_id == GameResult.id)
        .filter(GamePlayer.player_id == player_id)
        .all()
    )
    
    total_games = len(results)
    wins = 0
    losses = 0
    wins_team1 = 0
    wins_team2 = 0
    sum_for = 0
    sum_against = 0
    sum_for_wins = 0
    
    for gp, gr in results:
        score_for = gr.team1_score if gp.team == 1 else gr.team2_score
        score_against = gr.team2_score if gp.team == 1 else gr.team1_score
        sum_for += score_for
        sum_against += score_against

        if score_for > score_against:
            wins += 1
            sum_for_wins += score_for
            if gp.team == 1:
                wins_team1 += 1
            else:
                wins_team2 += 1
        else:
            losses += 1

    win_rate = (wins / total_games * 100) if total_games else 0
    avg_for = (sum_for / total_games) if total_games else 0
    avg_against = (sum_against / total_games) if total_games else 0
    avg_for_wins = (sum_for_wins / wins) if wins else 0

    return PlayerStats(
        total_games=total_games,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        wins_team1=wins_team1,
        wins_team2=wins_team2,
        avg_score_for=avg_for,
        avg_score_against=avg_against,
        avg_score_for_wins=avg_for_wins
    )